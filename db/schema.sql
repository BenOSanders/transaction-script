
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY NOT NULL,
    account_id TEXT,
    item_id FOREIGN KEY,
    amount REAL NOT NULL,
    description TEXT NOT NULL,
    date TEXT NOT NULL,
    merchant_name TEXT NOT NULL,
    address TEXT NOT NULL,
    zipcode TEXT NOT NULL,
    category TEXT,
    plaid TEXT NOT NULL,
    pending BOOL NOT NULL,
    notes TEXT
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
):
            
CREATE TABLE IF NOT EXISTS sync_state (
    account_id FOREIGN KEY,
    cursor TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
):
            
CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT NOT NULL PRIMARY KEY,
    item_id FOREIGN KEY,
    account_type TEXT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);
            
CREATE TABLE IF NOT EXISTS items (
    item_id TEXT UNIQUE NOT NULL,
    account_name TEXT NOT NULL,
    balance REAL NOT NULL,
    access_token TEXT NOT NULL,
);
