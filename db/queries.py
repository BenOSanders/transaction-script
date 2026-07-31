from datetime import datetime

from config import DB_PATH, Account, Item, SyncState, Transaction
from db.connection import get_connection

################
# Transactions #
################


def get_transaction(i: Item) -> Transaction:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    tsx = cu.execute(
        "SELECT * FROM transactions WHERE item_id = ?;", i.item_id
    ).fetchone()
    cu.close()
    cx.close()
    return tsx


def get_all_transactions() -> dict:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    rows = cu.execute("SELECT * FROM transactions ORDER BY date DESC").fetchall()
    transactions = [dict(row) for row in rows]
    cu.close()
    cx.close()
    return transactions


## Upsert transactions
def upsert_transactions(transactions) -> None:
    """
    Inputs many transactions into the database
    @param t: tuple of TransactionResponse objects ({transaction-1}, ..., {transaction-n})
    """

    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    for t in transactions:
        cu.execute(
            """INSERT INTO transactions (transaction_id, account_id, amount, description, date, merchant_name, address, zipcode, category, plaid, pending, notes) 
                   VALUES (:transaction_id, :account_id, :amount, :description, :date, :merchant_name, :address, :zipcode, :category, :plaid, :pending, :notes)
                   ON CONFLICT(transaction_id) DO UPDATE SET
                        account_id = excluded.account_id,
                        amount = excluded.amount,
                        description = excluded.description,
                        date = excluded.date,
                        merchant_name = excluded.merchant_name,
                        address = excluded.address,
                        zipcode = excluded.zipcode,
                        category = excluded.category,
                        plaid = excluded.plaid,
                        pending = excluded.pending,
                        notes = excluded.notes;
                    """,
            {
                "transaction_id": t.transaction_id,
                "account_id": t.account_id,
                "amount": t.amount,
                "description": t.name,
                "date": t.date,
                "merchant_name": t.merchant_name,
                "address": t.address,
                "zipcode": t.zipcode,
                "category": t.category,
                "plaid": t.plaid_category,
                "pending": t.pending,
                "notes": "",
            },
        )
    cx.commit()
    cu.close()
    cx.close()


## Delete transactions
def delete_transactions(transactions: list[Transaction]) -> bool:
    """
    should only be used interanlly, not exposed via API. Only for deleteing transactions from Plaid's transaction pull. Don't see any reason for users to delete transactions since transactions come directly from Plaid.
    """
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    cu.executemany(
        "DELETE FROM transactions WHERE transaction_id = ?;",
        [(id,) for transaction_id in transactions],
    )
    cx.commit()
    cu.close()
    cx.close()


##############
# Sync State #
##############


## Get cursor
def get_cursor(item_id: str) -> SyncState:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    re = cu.execute("SELECT * FROM sync_state WHERE item_id = ?", (item_id,)).fetchone()

    item_cursor: SyncState = SyncState(item_id=item_id)
    if re:
        item_cursor.cursor = re["cursor"]
        item_cursor.date = re["date"]
        item_cursor.sync_id = re["sync_id"]
    else:
        item_cursor.cursor = ""
        item_cursor.date = datetime.now().strftime("Y-%m-%d")
        item_cursor.sync_id = ""

    print(item_cursor)
    cu.close()
    cx.close()
    return item_cursor


## Set Cursor
def set_cursor(c: SyncState) -> None:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    cu.execute(
        """INSERT INTO sync_state (item_id, cursor, date)
            VALUES (:item_id, :cursor, :date)
            ON CONFLICT(sync_id) DO UPDATE SET
                item_id = excluded.item_id,
                cursor = excluded.cursor,
                date = excluded.date
    ;""",
        {"item_id": c.item_id, "cursor": c.cursor, "date": c.date},
    )
    cx.commit()
    cu.close()
    cx.close()


############
# Accounts #
############


## Get account
def get_account(a: Account) -> Account:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    res = cu.execute("SELECT * FROM accounts WHERE account_id = ?", a.account_id)
    row = res.fetchone()
    account: Account = Account(
        account_id=row["account_id"],
        item_id=row["item_id"],
        name=row["account_name"],
        balance=row["balance"],
        type=row["type"],
    )
    cu.close()
    cx.close()
    return account


## Get all accounts
def get_all_accounts() -> dict:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    rows = cu.execute("SELECT * FROM accounts").fetchall()  # Sqlite3 Row object
    accounts = [dict(row) for row in rows]  # Convert Row to Dict
    cu.close()
    cx.close()
    return accounts


## Insert account
def insert_account(a: Account):
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    cu.execute(
        "INSERT INTO accounts (account_id, item_id, account_name, balance, account_type) VALUES (:account_id, :item_id, :account_name, :balance, :account_type)",
        {
            "account_id": a.account_id,
            "item_id": a.item_id,
            "account_name": a.name,
            "balance": a.balance,
            "account_type": a.type,
        },
    )
    cx.commit()
    cu.close()
    cx.close()


########
# Item #
########


## Insert item
def insert_item(i: Item) -> None:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    cu.execute("INSERT INTO items VALUES (?, ?)", (i.item_id, i.access_token))
    cx.commit()
    cu.close()
    cx.close()


## Get all items
def get_all_items():
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    rows = cu.execute("SELECT * FROM items").fetchall()
    items = [dict(row) for row in rows]
    cu.close()
    cx.close()
    return items


########
# Misc #
########


## Get Balance
def get_balance(i: Item) -> float:
    cx = get_connection(DB_PATH)
    cu = cx.cursor()
    res = cu.execute("SELECT balance FROM items WHERE item_id = ?", i.item_id)
    cu.close()
    cx.close()
    return res["balance"]
