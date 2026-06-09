from app.db.connection import get_connection
from models import Transaction, Account, SyncState, Item
from config import DB_PATH
from sqlite3 import Row

# Transactions
def get_transactions(i: Item) -> Row:
    """

    """
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    return cu.execute("SELECT * FROM transactions WHERE item_id = ?;", i.item_id).fetchone()


## Upsert transactions
def upsert_transactions(t: Transaction) -> None:
    """
    Inputs many transactions into the database using executemany()
    @param t: tuple of transaction objects ({transaction-1}, ..., {transaction-n})
    """

    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    cu.executemany("""INSERT INTO transactions (transaction_id, account_id, amount, description, date, merchant_name, address, zipcode, category, plaid_category, pending, notes) 
                    VALUES (:transaction_id, :account_id, :amount, :description, :date, :merchant_name, :address, :zipcode, :category, :plaid_category, :pending, :notes
                    ON CONFLICT(transaction_id) DO UPDATE SET
                    account_id = excluded.account_id,
                    amount = excluded.amount,
                    description = excluded.description,
                    date = excluded.date,
                    merchant_name = excluded.merchant_name,
                    address = excluded.address,
                    zipcode = excluded.zipcode,
                    category = excluded.category,
                    plaid_category = excluded.plaid_category,
                    pending = excluded.pending,
                    notes = excluded.notes;
                    """,
                   {"transaction_id": t.transaction_id, "account_id": t.account_id, "amount": t.amount, "description": t.description, "date": t.date, "merchant_name": t.merchant_name, "address": t.address, "zipcode": t.zipcode, "category": t.category, "plaid_category": t.plaid_category, "pending": t.pending, "notes": t.notes})

## Delete transactions
def delete_transaction(t: Transaction) -> bool:
    """
    should only be used interanlly, not exposed via API. Only for deleteing transactions from Plaid's transaction pull. Don't see any reason for users to delete transactions since transactions come directly from Plaid. 
    """
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    cu.execute("DELETE * FROM transactions WHERE transaction_id = ?;", t.transaction_id)


# Sync State
## Get cursor
def get_cursor(i: Item) -> SyncState:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    re = cu.execute("SELECT * FROM sync_state WHERE item_id = ?;", i.item_id)
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
    ;""")


# Accounts
## Get accounts
def get_account(a: Account) -> Account:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    res = cu.execute("SELECT * FROM accounts WHERE account_id = ?", a.account_id)

## Insert account
def insert_account(a: Account) -> None:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    cu.execute("INSERT INTO accounts VALUES (?, ?, ?)", (a.account_id, a.item_id, a.type))

# Items
## Get Item(s) for a given Account ID


## Insert Item
def insert_account(i: Item) -> None:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    cu.execute("INSERT INTO items VALUES (?, ?, ?, ?)", (i.item_id, i.name, i.balance, i.access_token))


## Get Balance
def get_balance(i: Item) -> float:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    res = cu.execute("SELECT balance FROM items WHERE item_id = ?", i.item_id)
    return res["balance"]