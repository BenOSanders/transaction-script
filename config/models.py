from datetime import UTC, datetime

from pydantic import BaseModel


# Plaid Data
class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    amount: float
    description: str
    date: str | None = None
    auth_date: str | None = None
    merchant_name: str | None = None
    merchant_id: str | None = None
    merchant_logo_url: str | None = None
    address: str | None = None
    zipcode: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    lat: float | None = None
    lon: float | None = None
    category: str | None = None
    plaid_category: str
    pending: bool
    import_date: str | None = datetime.now(UTC).strftime(r"%y-%m-%d")
    notes: str | None = None


class SyncState(BaseModel):
    item_id: str
    cursor: str | None = ""
    updated_at: str | None = datetime.now(UTC).strftime(r"y-%m-%d %H:%M:%S")


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
