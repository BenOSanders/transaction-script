import plaid
from plaid.api import plaid_api
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.accounts_get_response import AccountsGetResponse
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_create_response import ItemPublicTokenCreateResponse
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.link_token_get_request import LinkTokenGetRequest
from plaid.model.link_token_get_response import LinkTokenGetResponse
from plaid.model.link_token_transactions import LinkTokenTransactions
from plaid.model.products import Products
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_sync_response import TransactionsSyncResponse

from config import (
    CLIENT_ID,
    ENVIRONMENT,
    PLAID_SECRET,
    USER_ID,
    Account,
    Item,
    SyncState,
)
from db import (
    get_all_items,
    get_cursor,
    insert_account,
    insert_item,
    set_cursor,
)

if ENVIRONMENT == "PRODUCTION": 
    ENV = plaid.Environment.Production
else:
    ENV = plaid.Environment.Sandbox

# Plaid Setup
configuration = plaid.Configuration(
    host=ENV,
    api_key={
        'clientId': CLIENT_ID,
        'secret': PLAID_SECRET
    }
)
plaid_api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(plaid_api_client) # API client where each endpoint returns dict which contains the parsed JSON from the HTTP res


def create_link_token():
    req = LinkTokenCreateRequest(
        products=[Products("transactions")],
        client_name="home-budget",
        country_codes=[CountryCode("US")],
        language="en",
         transactions=LinkTokenTransactions(
            days_requested=730
        ),
        user=LinkTokenCreateRequestUser(
            client_user_id=USER_ID
        )
    )
    res = client.link_token_create(req)
    return { "link_token": res.link_token }

# Get public token
def get_link_token():
    req = LinkTokenGetRequest()
    res:LinkTokenGetResponse = client.link_token_get(req)
    return res.to_dict()
    

# exchange public token
def exchange_public_token(public_token: str) -> tuple[str, str]:
    ''' Accepts a public token and exhcanges it with Plaid API for access token. 
        Stores that access token and associated item ID in DB, and returns the item ID. 
    '''
    req = ItemPublicTokenExchangeRequest(public_token=public_token)
    res : ItemPublicTokenCreateResponse = client.item_public_token_exchange(req)
    item = Item(
        item_id=res.item_id,
        access_token=res.access_token
    )
    insert_item(item)
    init_account(item)
    return res.item_id

def init_account(item: Item):
    # get account data
    req = AccountsGetRequest(
        access_token=item.access_token
    )
    res: AccountsGetResponse = client.accounts_get(req)
    for account in res.accounts:
        if account.balances.available:
            balance = account.balances.available
        else:
            balance = account.balances.current

        new_account = Account(
            account_id=account.account_id,
            item_id=item.item_id,
            name=account.name,
            balance=balance,
            type=str(account.type)
        )
        insert_account(new_account) # inconsitent bevaior with how I load transactions


def sync_plaid_transactions() -> dict:
    items = get_all_items()
    for item in items:
        cursor: SyncState = get_cursor(item["item_id"])
        request = TransactionsSyncRequest(
            access_token=item["access_token"],
            cursor=cursor.cursor if cursor.cursor else ''
        )
        #print(request)
        
        response: TransactionsSyncResponse = client.transactions_sync(request)
        data = response.to_dict()
        added_tx = data['added']
        modified_tx = data['modified']
        deleted_tx = data['removed']

        while(data['has_more']):
            request = TransactionsSyncRequest(
                access_token=item["access_token"],
                cursor=response['next_cursor']
            )
            print(request)
            response: TransactionsSyncRequest = client.transactions_sync(request)
            data = response.to_dict()
            added_tx += data['added']
            modified_tx += data['modified']
            deleted_tx += data['removed']

        new_cursor: SyncState = SyncState(item_id=item["item_id"], cursor=data["next_cursor"])
        # Update cursor
        set_cursor(new_cursor)
        return {"Added Transactions": added_tx, "Modified Transactions": modified_tx, "Deleted Transactions": deleted_tx, "Cursor": new_cursor}