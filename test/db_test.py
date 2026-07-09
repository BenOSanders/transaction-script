import sqlite3
conn = sqlite3.connect("../bank.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()


#cur.execute("SELECT sql FROM sqlite_master WHERE type='table'")
#for row in cur.fetchall():
#    print(row[0])

cur.execute("SELECT * FROM items")
for row in cur.fetchall():
    print(dict(row))