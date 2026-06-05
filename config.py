from dotenv import load_dotenv
import os

load_dotenv()

ENVIRONMENT = os.environ.get("ENVIRONMENT")
CLIENT_ID = os.environ.get("CLIENT_ID")
PLAID_SECRET = os.environ.get("PLAID_SECRET")