from fastapi import APIRouter
from pydantic import BaseModel

from db import get_all_transactions

router = APIRouter()


class TransactionUpdate(BaseModel):
    transaction_id: str
    update_field: str
    update_value: str | float


# Get transactions
@router.get("/transactions")
def read_transactions():
    transactions = get_all_transactions()
    return transactions
