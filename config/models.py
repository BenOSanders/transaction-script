from datetime import datetime

from pydantic import BaseModel


# Plaid Data
class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    amount: float
    description: str
    date: str | None = None
    auth_date: str | None = None
    merchant_name: str
    address: str | None = None
    zipcode: str | None = None
    category: str | None = None
    plaid_category: str
    pending: bool
    notes: str | None = None


class SyncState(BaseModel):
    sync_id: str | None = ""
    item_id: str
    cursor: str | None = ""
    date: str | None = datetime.now().strftime(r"y-%m-%d %H:%M:%S")


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
