from db import get_all_accounts
from fastapi import APIRouter, HTTPException
import json

router = APIRouter()

# Get transactions
@router.get("/accounts")
def read_accounts():
    accounts = get_all_accounts() # Dict returned
    return accounts # Dict converted to JSON by FastAPI

