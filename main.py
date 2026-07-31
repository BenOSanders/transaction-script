
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import DB_PATH
from db import init_db
from routers import accounts, plaid, transactions

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