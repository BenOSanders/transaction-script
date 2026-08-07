from datetime import UTC, datetime

from config import Transaction
from db import delete_transactions, set_cursor, upsert_transactions
from plaid_client import sync_plaid_transactions


def sync_transactions():
    """Called by sync API endpoint. Runs Plaid Sync Transactions function to get transaction data from Plaid,
    then passed it to db.
    """
    plaid_updates = sync_plaid_transactions()

    added = to_transaction_model(plaid_updates["Added Transactions"])
    modified = to_transaction_model(plaid_updates["Modified Transactions"])
    deleted = to_transaction_model(plaid_updates["Deleted Transactions"])

    upsert_transactions(added)
    upsert_transactions(modified)
    delete_transactions(deleted)
    set_cursor(plaid_updates["Cursor"])


def to_transaction_model(transactions: list) -> list:
    """
    Converts dict from Plaid's API into pydnatic transaction data model.
    """
    processed_transactions = []
    for t in transactions:
        processed_transactions.append(
            Transaction(
                transaction_id=t["transaction_id"],
                account_id=t["account_id"],
                amount=t["amount"],
                description=t["name"],
                date=datetime.strftime(t["date"], r"%y-%m-%d")
                if t["date"]
                else "",
                auth_date=datetime.strftime(t["authorized_date"], r"%y-%m-%d")
                if t["authorized_date"]
                else "",
                merchant_name=t["merchant_name"],
                merchant_id=t["merchant_id"],
                merchant_logo_url=t["merchant_logo_url"],
                address=t["location"]["address"],
                zipcode=t["location"]["postal_code"],
                city=t["city"],
                state=t["state"],
                country=t["country"],
                lat=t["lat"],
                lon=t["lon"],
                category="",
                plaid_category=t["personal_finance_category"]["primary"],
                pending=t["pending"],
                import_date=datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
                notes="",
            )
        )

    return processed_transactions
