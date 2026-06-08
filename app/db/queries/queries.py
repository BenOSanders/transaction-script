from db import get_connection
from models import Transaction, Account, SyncState, Item
from config import DB_PATH
from sqlite3 import Row

# Transactions
def get_transactions(t: Transaction) -> Row:
    """

    """
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    return cu.execute("SELECT * FROM transactions").fetchone()


## Upsert transactions
def upsert_transactions(t: tuple) -> None:
    """
    Inputs many transactions into the database using executemany()
    @param t: tuple of transaction objects ({transaction-1}, ..., {transaction-n})
    """

    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    cu.executemany("INSERT OR REPLACE INTO transactions (transaction_id, account_id, amount, description, date, merchant_name, address, zipcode, category, plaid_category, pending, nodes)" \
    "VALUES(:transaction_id, :account_id, :amount, :description, :date, :merchant_name, :address, :zipcode, :category, :plaid_category, :pending, :notes" \
    "ON CONFLICT(transaction_id) DO UPDATE SET" \
    "account_id = excluded.account_id" \
    "amount = excluded.amount, " \
    "description = excluded.description, " \
    "date = excluded.date, " \
    "merchant_name = excluded.merchant_name, " \
    "address = excluded.address, " \
    "zipcode = excluded.zipcode, " \
    "category = excluded.category, " \
    "plaid_category = excluded.plaid_category, " \
    "pending = excluded.pending, " \
    "notes = excluded.notes" \
    ")", t)

## Delete transactions
def delete_transaction(t: Transaction) -> bool:



# Sync State
## Get cursor
def get_cursor(i: Item) -> SyncState:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    re = cu.execute("SELECT * FROM sync_state WHERE item_id = ?", i.item_id)
    item_cursor: SyncState
    item_cursor.cursor = re.cursor
    item_cursor.account_id = re.account_id
    return item_cursor

## Set Cursor
def set_cursor(c: SyncState) -> None:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    cu.execute("""INSERT INTO sync_state (item_id, cursor)
            VALUES (@item_id, @cursor)
            ON CONFLICT(item_id) DO UPDATE SET
                cursor = excluded.cursor
    """)


# Accounts
## Get accounts

## Insert account


# Items
## Get Item(s) for a given Account ID

## Insert Item

## Get Balance
def get_balance(i: Item) -> float:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    res = cu.execute("SELECT balance FROM items WHERE item_id = ?", i.item_id)
    return res["balance"]