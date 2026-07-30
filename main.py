from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config import Item
from sqlite3 import Row
from routers import transactions, plaid, accounts
from db import init_db
from config import DB_PATH

init_db(DB_PATH)

# Fast API Setup
app = FastAPI()

app.include_router(transactions.router, prefix="/api")
app.include_router(plaid.router, prefix="/api")
app.include_router(accounts.router, prefix="/api")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

#@app.get('/')
#def root():
#    return {"html": ./static/index.html}