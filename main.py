from config import ENVIRONMENT, CLIENT_ID, PLAID_SECRET
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


def get_transactions():
    try:
        
    except:

def main():

    # 


if __name__ == "__main__":
    main()