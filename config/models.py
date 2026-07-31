from datetime import datetime

from plaid.model.transactions_sync_response import TransactionsSyncResponse
from pydantic import BaseModel


# Plaid Data
class Transaction(TransactionsSyncResponse):
    transaction_id: str
    account_id: str
    amount: float
    description: str
    date: str
    auth_date: str
    merchant_name: str
    address: str
    zipcode: str
    category: str | None = None
    plaid_category: str
    pending: bool
    notes: str | None = None


class SyncState(BaseModel):
    sync_id: str | None = ""
    item_id: str
    cursor: str | None = ""
    date: str | None = datetime.now().strftime(r"Y-%m-%d %H:%M:%S")


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
