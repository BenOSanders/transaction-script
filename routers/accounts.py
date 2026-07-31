from fastapi import APIRouter

from db import get_all_accounts

router = APIRouter()


# Get transactions
@router.get("/accounts")
def read_accounts():
    accounts = get_all_accounts()  # Dict returned
    return accounts  # Dict converted to JSON by FastAPI
