from db import upsert_transactions, delete_transactions, set_cursor
from plaid_client import sync_plaid_transactions

def sync_transactions():
    """Called by sync API endpoint. Runs Plaid Sync Transactions function to get transaction data from Plaid, 
    then passed it to db.
    """
    plaid_updates = sync_plaid_transactions()
    set_cursor(plaid_updates["Cursor"])
    upsert_transactions(plaid_updates["Added Transactions"])
    upsert_transactions(plaid_updates["Modified Transactions"])
    delete_transactions(plaid_updates["Deleted Transactions"])
