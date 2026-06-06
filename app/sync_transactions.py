import plaid
from plaid.model.transactions_sync_request import TransactionsSyncRequest

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

    # pass into function to add to DB