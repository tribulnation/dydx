from typing_extensions import Literal, overload, AsyncIterable, Sequence
from dataclasses import dataclass
from datetime import datetime

from dydx.core import timestamp as ts, TypedDict
from .core import IndexerMixin, response_parser, Response

class Fill(TypedDict):
  ...

class Fills(TypedDict):
  fills: list[Fill]

parse_response = response_parser(Fills)

@dataclass
class GetFills(IndexerMixin):
  @overload
  async def get_fills(
    self, address: str, *,
    subaccount: int = 0,
    ticker: str | None = None,
    end_height: int | None = None,
    end: datetime | None = None,
    page: int | None = None,
    limit: int | None = None,
    validate: bool | None = None,
    unsafe: Literal[True] = True,
  ) -> Fills:
    ...
  @overload
  async def get_fills(
    self, address: str, *,
    subaccount: int = 0,
    ticker: str | None = None,
    end_height: int | None = None,
    end: datetime | None = None,
    page: int | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> Response[Fills]:
    ...
  async def get_fills(
    self, address: str, *,
    subaccount: int = 0,
    ticker: str | None = None,
    end_height: int | None = None,
    end: datetime | None = None,
    limit: int | None = None,
    page: int | None = None,
    validate: bool | None = None,
    unsafe: bool = False,
  ) -> Response[Fills] | Fills:
    """Retrieves fill records for a specific subaccount on the exchange. A fill represents a trade that has been executed.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `ticker`: The market ticker (e.g. `'BTC-USD'`).
    - `end_height`: If given, fetches fills up to and including the given block height.
    - `end`: If given, fetches fills up to and including the given timestamp.
    - `limit`: The max. number of fills to retrieve (default: 1000, max: 1000).
    - `page`: 	The page number for paginated results (default: 1).
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-fills)
    """
    params = {'address': address, 'subaccountNumber': subaccount}
    if ticker is not None:
      params['ticker'] = ticker
    if end_height is not None:
      params['createdBeforeOrAtHeight'] = end_height
    if end is not None:
      params['createdBeforeOrAt'] = ts.dump(end)
    if limit is not None:
      params['limit'] = limit
    if page is not None:
      params['page'] = page
    r = await self.request('GET', '/v4/fills', params=params)
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))

  
  async def get_fills_paged(
    self, address: str, *,
    subaccount: int = 0,
    ticker: str | None = None,
    end_height: int | None = None,
    end: datetime | None = None,
    limit: int | None = None,
  ) -> AsyncIterable[list[Fill]]:
    page = 1
    while True:
      r = await self.get_fills(address, subaccount=subaccount, ticker=ticker, end_height=end_height, end=end, limit=limit, page=page, unsafe=True)
      if not r['fills']:
        break
      yield r['fills']
      page += 1