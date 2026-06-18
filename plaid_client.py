import plaid
from plaid.api import plaid_api
from plaid.model.link_token_transactions import LinkTokenTransactions
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.link_token_create_hosted_link import LinkTokenCreateHostedLink
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from config import ENVIRONMENT, CLIENT_ID, PLAID_SECRET, ACCESS_TOKEN, USER_ID
from db import upsert_transactions, delete_transactions

if ENVIRONMENT == "PRODUCTION": 
    ENV = plaid.Environment.Production
else:
    ENV = plaid.Environment.Sandbox

# Plaid Setup
configuration = plaid.Configuration(
    host=ENV,
    api_key={
        'clientId': CLIENT_ID,
        'secret': PLAID_SECRET
    }
)
plaid_api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(plaid_api_client) # API client where each endpoint returns dict which contains the parsed JSON from the HTTP res


def create_link_token():
    req = LinkTokenCreateRequest(
        products=[Products("transactions")],
        client_name="home-budget",
        country_codes=[CountryCode("US")],
        language="en",
         transactions=LinkTokenTransactions(
            days_requested=730
        ),
        user=LinkTokenCreateRequestUser(
            client_user_id=USER_ID
        ),
        hosted_link=LinkTokenCreateHostedLink(
        )
    )
    res = client.link_token_create(req)
    return {"hosted_link_url": res["hosted_link_url"]}

# Get link token

# exchange public token
def exchange_public_token(public_token: str) -> tuple[str, str]:
    req = ItemPublicTokenExchangeRequest(public_token=public_token)
    res = client.item_public_token_exchange(req)
    return res["access_token"], res["item_id"]


def sync_plaid_transactions():
    request = TransactionsSyncRequest(
        access_token=ACCESS_TOKEN,
    )
    response = client.transactions_sync(request)
    new_and_modified_tx = response['added']
    new_and_modified_tx += response['modified']
    deleted_tx = response['removed']

    while(response['has_more']):
        request = TransactionsSyncRequest(
            access_token=ACCESS_TOKEN,
            cursor=response['next_cursor']
        )
        response = client.transactions_sync(request)
        new_and_modified_tx += response['added']
        new_and_modified_tx += response['modified']
        deleted_tx += response['removed']



    # pass into function to put into tuple of Transactions pydanic type for passing to upsert_transactions(t: tuple)
    upsert_transactions(new_and_modified_tx)
    delete_transactions(deleted_tx);
