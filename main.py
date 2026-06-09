from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from db import queries
from config import Item
from sqlite3 import Row

from db import init_db

app = FastAPI()


@app.post("/transactions/sync")
def sync_transactions():
    # Sync plaid transactions

@app.get("/transactions/")
def get_all_transactions():
    # Get all transactions

@app.get("/transactions/{transaction_id}"):
def get_transaction(item_id: Item):
    # Get specific transaction
    transactions: Row = queries.get_transactions(item_id) # returns sqlite3 row object
    return transactions