from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    sync_id: Optional[str] = ''
    item_id: str
    cursor: Optional[str] = ''
    date: Optional[str] = datetime.now().strftime(r"Y-%m-%d %H:%M:%S")

class Account(BaseModel):
    account_id: str
    item_id: str
    name: str
    balance: float = 0.0
    type: str

class Item(BaseModel):
    item_id: str
    access_token: str


# API Data Models