from typing_extensions import Literal, AsyncIterable, NotRequired
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from dydx.core import timestamp as ts, TypedDict
from dydx.indexer.types import OrderSide, PositionSide, FillType, Liquidity
from .core import IndexerMixin, response_parser

class Fill(TypedDict):
  id: str
  side: OrderSide
  liquidity: Liquidity
  type: FillType
  market: str
  price: Decimal
  size: Decimal
  fee: Decimal
  affiliateRevShare: Decimal
  createdAt: datetime
  createdAtHeight: int
  orderId: NotRequired[str|None]
  clientMetadata: NotRequired[str|None]
  subaccountNumber: int
  builderFee: NotRequired[Decimal|None]
  builderAddress: NotRequired[str|None]
  positionSizeBefore: NotRequired[Decimal|None]
  entryPriceBefore: NotRequired[Decimal|None]
  positionSideBefore: NotRequired[PositionSide|None]

class Fills(TypedDict):
  fills: list[Fill]

parse_response = response_parser(Fills)

MarketType = Literal['PERPETUAL', 'SPOT']

@dataclass
class GetFills(IndexerMixin):
  async def get_fills(
    self, address: str, *,
    subaccount: int = 0,
    market: str | None = None,
    market_type: MarketType | None = None,
    end_height: int | None = None,
    end: datetime | None = None,
    limit: int | None = None,
    page: int | None = None,
    validate: bool | None = None,
  ) -> list[Fill]:
    """Retrieves fill records for a specific subaccount on the exchange. A fill represents a trade that has been executed.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `market`: The market name (e.g. `'BTC-USD'`).
    - `market_type`: The market type (`'PERPETUAL'` or `'SPOT'`). Must be provided if `market` is provided.
    - `end_height`: If given, fetches fills up to and including the given block height.
    - `end`: If given, fetches fills up to and including the given timestamp.
    - `limit`: The max. number of fills to retrieve (default: 1000, max: 1000).
    - `page`: 	The page number for paginated results (default: 1).
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-fills)
    """
    params = {'address': address, 'subaccountNumber': subaccount}
    if market is not None:
      params['market'] = market
    if market_type is not None:
      params['marketType'] = market_type
    if end_height is not None:
      params['createdBeforeOrAtHeight'] = end_height
    if end is not None:
      params['createdBeforeOrAt'] = ts.dump(end)
    if limit is not None:
      params['limit'] = limit
    if page is not None:
      params['page'] = page
    r = await self.request('GET', '/v4/fills', params=params)
    return parse_response(r, validate=self.validate(validate))['fills']

  
  async def get_fills_paged(
    self, address: str, *,
    subaccount: int = 0,
    market: str | None = None,
    market_type: MarketType | None = None,
    end_height: int | None = None,
    end: datetime | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> AsyncIterable[list[Fill]]:
    """Retrieves fill records for a specific subaccount on the exchange. A fill represents a trade that has been executed.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `market`: The market name (e.g. `'BTC-USD'`).
    - `market_type`: The market type (`'PERPETUAL'` or `'SPOT'`). Must be provided if `market` is provided.
    - `end_height`: If given, fetches fills up to and including the given block height.
    - `end`: If given, fetches fills up to and including the given timestamp.
    - `limit`: The max. number of fills to retrieve (default: 1000, max: 1000).
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-fills)
    """
    page = 1
    while True:
      fills = await self.get_fills(address, subaccount=subaccount, market=market, market_type=market_type, end_height=end_height, end=end, limit=limit, page=page, validate=validate)
      if not fills:
        break
      yield fills
      page += 1