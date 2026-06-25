from pydantic import BaseModel
from typing import Optional
# import datetime

# Plaid Data Models
class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    amount: float
    description: str
    date: str
    merchant_name: str
    address: str
    zipcode: str
    category: Optional[str] = None
    plaid_category: str
    pending: bool
    notes: Optional[str] = None

class SyncState(BaseModel):
    accont_id: str
    cursor: str

class Account(BaseModel):
    account_id: str
    item_id: str
    name: str
    balance: float
    type: str

class Item(BaseModel):
    item_id: str
    access_token: str


# API Data Models