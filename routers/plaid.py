import plaid
from fastapi import APIRouter
from db import get_all_transactions
from plaid_client import sync_plaid_transactions, create_link_token, get_link_token, exchange_public_token
from config import Item

router = APIRouter()

@router.post("/sync")
def sync_transactions():
    # call sync function
    sync_plaid_transactions()
    return
#
#@router.get("/transactions")
#def read_transactions() -> dict:
#    transactions = get_all_transactions()
#    return dict(transactions)

@router.get("/link")
async def link_account():
    return await create_link_token()

@router.post("/import-new-items")
def import_items():
    # We have an access token
    added_items_list = get_link_token()["results"]["item_add_results"]
    prepared_items = list(Item)
    for item in added_items_list:
        # process data for each. Insert into pydantic Item object, then add to 
        prepared_items.append(
            Item(
                item_id=item['item_id'],
                name=item['institution']['name']
            )
        )

@router.post("/create-link-token")
def create_link_token():
    pass

@router.post("/exchange")
def exchange():
    pass