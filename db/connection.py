import sqlite3


def get_connection(db_path):
    cx = sqlite3.connect(db_path)
    cx.row_factory = sqlite3.Row
    cx.execute("PRAGMA foreign_keys = ON;")
    cx.execute("PRAGMA journal_mode = ON;")
    return cx

def init_db(db_path):
    cx = get_connection(db_path)
    with open("db/schema.sql", "r") as f:
        cx.executescript(f.read())
    cx.close()