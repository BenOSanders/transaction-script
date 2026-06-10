import plaid
from fastapi import APIRouter
from db import get_all_transactions

# this set of routers connects to plaid_client and queries to interact with plaid and db

router = APIRouter()

@router.post("/sync")
def sync_transactions():
    # call sync function
    return

@router.get("/transactions")
def read_transactions() -> dict:
    transactions = get_all_transactions()
    return dict(transactions)