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
class GetParentSubaccountFills(IndexerMixin):
  async def get_parent_subaccount_fills(
    self,
    address: str,
    *,
    parent_subaccount: int,
    ticker: str | None = None,
    ticker_type: Literal['PERPETUAL', 'SPOT'] | None = None,
    limit: int | None = None,
    created_before_or_at_height: int | None = None,
    created_before_or_at: datetime | None = None,
    page: int | None = None,
    validate: bool | None = None
  ) -> FillsResponse:
    """
    Get parent subaccount fills

    - `address`: Wallet address that owns the account.
    - `parent_subaccount`: Parent subaccount number.
    - `ticker`: Ticker filter.
    - `ticker_type`: Ticker type filter.
    - `limit`: Maximum number of results to return.
    - `created_before_or_at_height`: Restrict results to entries created at or before a specific block height.
    - `created_before_or_at`: Restrict results to entries created at or before a specific timestamp.
    - `page`: Page number for paginated results.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/accounts#get-parent-subaccount-number-fills)
    """
    params: dict[str, object] = {
      'address': address,
      'parentSubaccountNumber': parent_subaccount,
    }
    if ticker is not None:
      params['ticker'] = ticker
    if ticker_type is not None:
      params['tickerType'] = ticker_type
    if limit is not None:
      params['limit'] = limit
    if created_before_or_at_height is not None:
      params['createdBeforeOrAtHeight'] = created_before_or_at_height
    if created_before_or_at is not None:
      params['createdBeforeOrAt'] = ts.dump(created_before_or_at)
    if page is not None:
      params['page'] = page
    r = await self.request('GET', '/v4/fills/parentSubaccountNumber', params=params)
    return parse_response(r, validate=self.validate(validate))
