import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from config import ENVIRONMENT, CLIENT_ID, PLAID_SECRET
from db import upsert_transactions, delete_transactions

# Plaid Setup
configuration = plaid.Configuration(
    host=ENVIRONMENT,
    api_key={
        'clientId': CLIENT_ID,
        'secret': PLAID_SECRET
    }
)
plaid_api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(plaid_api_client) # API client where each endpoint returns dict which contains the parsed JSON from the HTTP res


def create_link_token():
    req = LinkTokenCreateRequest(
        products=["transactions"],
        client_name="home-budget",
        country_codes=["US"],
        language="US"
    )
    res = client.link_token_create(req)
    return res["link_token"]

# exchange public token
def exchange_public_token(public_token: str) -> tuple[str, str]:
    req = ItemPublicTokenExchangeRequest(public_token=public_token)
    res = client.item_public_token_exchange(req)
    return res["access_token"], res["item_id"]


def sync_transactions(client):
    request = TransactionsSyncRequest(
        access_token="",
    )
    response = client.transaction_sync(request)
    new_and_modified_tx = response['added']
    new_and_modified_tx += response['modified']
    deleted_tx = response['removed']

    while(response['has_more']):
        request = TransactionsSyncRequest(
            access_token="",
            cursor=response['next_cursor']
        )
        response = client.transactions_sync(request)
        new_and_modified_tx += response['added']
        new_and_modified_tx += response['modified']
        deleted_tx += response['removed']



    # pass into function to put into tuple of Transactions pydanic type for passing to upsert_transactions(t: tuple)
    upsert_transactions(new_and_modified_tx)
    delete_transactions(deleted_tx);
