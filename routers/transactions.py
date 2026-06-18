from db import get_all_transactions
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Get transactions
@router.get("/transactions")
def read_transactions():
    return get_all_transactions()

