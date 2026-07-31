import os

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT")
CLIENT_ID = os.environ.get("CLIENT_ID")
PLAID_SECRET = os.environ.get("PLAID_SECRET")
DB_PATH = os.environ.get("DB_PATH")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
USER_ID = os.environ.get("USER_ID")
