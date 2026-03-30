from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from dydx.core import timestamp as ts
from typing_extensions import Literal, NotRequired, TypedDict
from ..core import IndexerMixin, response_parser

class Fill(TypedDict):
  id: str
  side: Literal['BUY', 'SELL']
  liquidity: Literal['MAKER', 'TAKER']
  type: Literal['LIMIT', 'LIQUIDATED', 'LIQUIDATION', 'DELEVERAGED', 'OFFSETTING']
  market: str
  marketType: Literal['PERPETUAL', 'SPOT']
  price: Decimal
  size: Decimal
  fee: Decimal
  affiliateRevShare: Decimal
  createdAt: datetime
  createdAtHeight: str
  orderId: NotRequired[str | None]
  clientMetadata: NotRequired[str | None]
  subaccountNumber: int
  builderFee: NotRequired[Decimal | None]
  builderAddress: NotRequired[str | None]
  positionSizeBefore: NotRequired[Decimal | None]
  entryPriceBefore: NotRequired[Decimal | None]
  positionSideBefore: NotRequired[Literal['LONG', 'SHORT'] | None]

class FillsResponse(TypedDict):
  fills: list[Fill]

parse_response = response_parser(FillsResponse)

@dataclass
class GetFills(IndexerMixin):
  async def get_fills(
    self,
    address: str,
    *,
    subaccount: int,
    market: str | None = None,
    market_type: Literal['PERPETUAL', 'SPOT'] | None = None,
    created_before_or_at_height: int | None = None,
    created_before_or_at: datetime | None = None,
    limit: int | None = None,
    page: int | None = None,
    validate: bool | None = None
  ) -> FillsResponse:
    """
    Retrieve fill records for a subaccount.

    - `address`: Wallet address that owns the subaccount.
    - `subaccount`: Subaccount number.
    - `market`: Market ticker filter.
    - `market_type`: Market type filter.
    - `created_before_or_at_height`: Latest block height to include.
    - `created_before_or_at`: Latest timestamp to include.
    - `limit`: Maximum number of fills to return.
    - `page`: Page number for paginated results.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http#get-fills)
    """
    params: dict[str, object] = {
      'address': address,
      'subaccountNumber': subaccount,
    }
    if market is not None:
      params['market'] = market
    if market_type is not None:
      params['marketType'] = market_type
    if created_before_or_at_height is not None:
      params['createdBeforeOrAtHeight'] = created_before_or_at_height
    if created_before_or_at is not None:
      params['createdBeforeOrAt'] = ts.dump(created_before_or_at)
    if limit is not None:
      params['limit'] = limit
    if page is not None:
      params['page'] = page
    r = await self.request('GET', '/v4/fills', params=params)
    return parse_response(r, validate=self.validate(validate))
