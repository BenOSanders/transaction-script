from app.config import ENVIRONMENT, CLIENT_ID, PLAID_SECRET
from app.sync_transactions import sync_transactions
import plaid
from plaid.api import plaid_api
import requests

configuration = plaid.Configuration(
    host=ENVIRONMENT,
    api_key={
        'clientId': CLIENT_ID,
        'secret': PLAID_SECRET
    }
)

api_client = plaid.ApiClient(configuration)

# API client where each endpoint returns dict which contains the parsed JSON from the HTTP res
client = plaid_api.PlaidApi(api_client)


def main():
    sync_transactions(client)


if __name__ == "__main__":
    main()