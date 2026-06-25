CREATE TABLE IF NOT EXISTS items (
    item_id TEXT PRIMARY KEY,
    access_token TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    item_id TEXT,
    account_name TEXT NOT NULL,
    balance REAL NOT NULL,
    account_type TEXT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    account_id TEXT,
    item_id TEXT,
    amount REAL NOT NULL,
    description TEXT NOT NULL,
    date TEXT NOT NULL,
    merchant_name TEXT NOT NULL,
    address TEXT NOT NULL,
    zipcode TEXT NOT NULL,
    category TEXT,
    plaid TEXT NOT NULL,
    pending BOOL NOT NULL,
    notes TEXT,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE IF NOT EXISTS sync_state (
    sync_id TEXT PRIMARY KEY,
    account_id TEXT,
    cursor TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
