import sqlite3

conn = sqlite3.connect("../bank.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("DELETE FROM transactions")
conn.commit()

# Close DB connection
cur.close()
conn.close()
