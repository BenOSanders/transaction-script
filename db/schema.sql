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
    description TEXT,
    date TEXT,
    auth_date TEXT,
    merchant_name TEXT,
    merchant_id TEXT,
    merchant_logo_url TEXT,
    address TEXT,
    zipcode TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    lat REAL,
    lon REAL,
    category TEXT,
    plaid TEXT NOT NULL,
    pending BOOL NOT NULL,
    import_date TEXT NOT NULL,
    notes TEXT,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE IF NOT EXISTS sync_state (
    item_id TEXT PRIMARY KEY REFERENCES items(item_id) ON DELETE CASCADE,
    cursor TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL
);
