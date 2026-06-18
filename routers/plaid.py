import plaid
from fastapi import APIRouter
from db import get_all_transactions
from plaid_client import sync_plaid_transactions, create_link_token

# this set of routers connects to plaid_client and queries to interact with plaid and db

router = APIRouter()

@router.post("/sync")
def sync_transactions():
    # call sync function
    sync_plaid_transactions()
    return
#
#@router.get("/transactions")
#def read_transactions() -> dict:
#    transactions = get_all_transactions()
#    return dict(transactions)

@router.get("/link")
async def link_account():
    return await create_link_token()