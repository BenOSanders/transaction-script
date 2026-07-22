from db import get_all_transactions
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Get transactions
@router.get("/transactions")
def read_transactions():
    transactions = get_all_transactions()
    print(transactions)
    return transactions
