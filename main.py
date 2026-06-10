from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from db import queries
from config import Item
from sqlite3 import Row
from routers import transactions, plaid, chat
from db import init_db


# Fast API Setup
app = FastAPI()

app.include_router(transactions.router, prefix="/api")
app.include_router(plaid.router, prefix="/api")

