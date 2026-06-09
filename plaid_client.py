import plaid
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid_client import sync_transactions
from plaid.api import plaid_api
from config import ENVIRONMENT, CLIENT_ID, PLAID_SECRET

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


def format_transactions(t: dict):
    """
    Takes dict of transactions and formats them into a tuple of Transactions
    """

def sync_transactions(client):
    request = TransactionsSyncRequest(
        access_token="",
    )
    response = client.transaction_sync(request)
    new_transactions = response['added']
    modified_transactions = response['modified']
    deleted_transactions = response['removed']

    while(response['has_more']):
        request = TransactionsSyncRequest(
            access_token="",
            cursor=response['next_cursor']
        )
        response = client.transactions_sync(request)
        new_transactions += response['added']
        modified_transactions += response['modified']
        deleted_transactions += response['removed']

    # pass into function to put into tuple of Transactions pydanic type for passing to upsert_transactions(t: tuple)

