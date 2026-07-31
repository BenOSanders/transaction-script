from fastapi import APIRouter
from pydantic import BaseModel

from config import Item
from plaid_client import (
    create_link_token,
    exchange_public_token,
    get_link_token,
)
from services import sync_transactions

router = APIRouter()


class ExchangeRequest(BaseModel):
    public_token: str


@router.post("/sync")
def sync():
    sync_transactions()


@router.post("/link")
def link_account():
    res = create_link_token()
    return {"status": "ok", "link_token": res}


@router.post("/import-new-items")
def import_items():
    # We have an access token
    added_items_list = get_link_token()["results"]["item_add_results"]
    prepared_items = list(Item)
    for item in added_items_list:
        # process data for each. Insert into pydantic Item object, then add to
        prepared_items.append(
            Item(item_id=item["item_id"], name=item["institution"]["name"])
        )


@router.post("/connect")
def connect(body: ExchangeRequest):
    """This function triggers a multi step process when adding a new bank account.
    1. Exhanges public token for access token.
    2. Run transaction sync that loads initial account info
    """
    item_id = exchange_public_token(body.public_token)
    # function to load in
    # load transactions
