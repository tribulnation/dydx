from typing_extensions import AsyncIterable, Literal
from dataclasses import dataclass
from datetime import datetime

from typed_core import PaginatedResponse
from .api.get_fills import GetFills, Fill

MarketType = Literal['PERPETUAL', 'SPOT']


@dataclass
class GetFillsPaged(GetFills):
  def get_fills_paged(
    self, address: str, *,
    subaccount: int,
    market: str | None = None,
    market_type: MarketType | None = None,
    created_before_or_at_height: int | None = None,
    created_before_or_at: datetime | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[Fill, int]:
    """Retrieves fill records for a specific subaccount on the exchange. A fill represents a trade that has been executed.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `market`: The market name (e.g. `'BTC-USD'`).
    - `market_type`: The market type (`'PERPETUAL'` or `'SPOT'`). Must be provided if `market` is provided.
    - `created_before_or_at_height`: If given, fetches fills up to and including the given block height.
    - `created_before_or_at`: If given, fetches fills up to and including the given timestamp.
    - `limit`: The max. number of fills to retrieve (default: 1000, max: 1000).
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-fills)
    """
    async def next(page: int) -> tuple[list[Fill], int | None]:
      response = await self.get_fills(
        address,
        subaccount=subaccount,
        market=market,
        market_type=market_type,
        created_before_or_at_height=created_before_or_at_height,
        created_before_or_at=created_before_or_at,
        limit=limit,
        page=page,
        validate=validate,
      )
      fills = response['fills']
      next_page = page + 1 if len(fills) == limit else None
      return fills, next_page

    return PaginatedResponse(1, next)
