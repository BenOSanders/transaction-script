from db import get_transactions
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Get transactions
@router.get("/transactions")
def read_transactions():
    return {get_transactions()}

