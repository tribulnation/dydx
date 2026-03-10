from typing_extensions import Literal, AsyncIterable, NotRequired
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from dydx.core import timestamp as ts, TypedDict
from dydx.indexer.types import TransferType
from .core import IndexerMixin, response_parser

class Account(TypedDict):
  address: str
  subaccountNumber: NotRequired[int]

class Transfer(TypedDict):
  id: str
  sender: Account
  recipient: Account
  size: Decimal
  createdAt: datetime
  createdAtHeight: int
  symbol: str
  type: TransferType
  transactionHash: str

class Transfers(TypedDict):
  transfers: list[Transfer]

parse_response = response_parser(Transfers)

@dataclass
class GetTransfers(IndexerMixin):
  async def get_transfers(
    self, address: str, *,
    subaccount: int = 0,
    end_height: int | None = None,
    end: datetime | None = None,
    limit: int | None = None,
    page: int | None = None,
    validate: bool | None = None,
  ) -> list[Transfer]:
    """Retrieves the transfer history for a specific subaccount.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `end_height`: If given, fetches transfers up to and including the given block height.
    - `end`: If given, fetches transfers up to and including the given timestamp.
    - `limit`: The max. number of transfers to retrieve (default: 1000, max: 1000).
    - `page`: 	The page number for paginated results (default: 1).
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-transfers)
    """
    params = {'address': address, 'subaccountNumber': subaccount}
    if end_height is not None:
      params['createdBeforeOrAtHeight'] = end_height
    if end is not None:
      params['createdBeforeOrAt'] = ts.dump(end)
    if limit is not None:
      params['limit'] = limit
    if page is not None:
      params['page'] = page
    r = await self.request('GET', '/v4/transfers', params=params)
    return parse_response(r, validate=self.validate(validate))['transfers']

  
  async def get_transfers_paged(
    self, address: str, *,
    subaccount: int = 0,
    end_height: int | None = None,
    end: datetime | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> AsyncIterable[list[Transfer]]:
    """Retrieves the transfer history for a specific subaccount.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `end_height`: If given, fetches transfers up to and including the given block height.
    - `end`: If given, fetches transfers up to and including the given timestamp.
    - `limit`: The max. number of transfers to retrieve (default: 1000, max: 1000).
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-transfers)
    """
    page = 1
    while True:
      transfers = await self.get_transfers(address, subaccount=subaccount, end_height=end_height, end=end, limit=limit, page=page, validate=validate)
      if not transfers:
        break
      yield transfers
      page += 1