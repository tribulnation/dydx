from dataclasses import dataclass
from datetime import datetime

from typed_core import PaginatedResponse
from .api.get_historical_funding import GetHistoricalFunding, Funding

@dataclass
class GetHistoricalFundingPaged(GetHistoricalFunding):
  def get_historical_funding_paged(
    self,
    market: str,
    *,
    effective_before_or_at: datetime | None = None,
    effective_before_or_at_height: int | None = None,
    limit: int | None = None,
  ) -> PaginatedResponse[Funding, int]:
    """Retrieves historical funding rates for a specific perpetual market, automatically paginating.

    - `market`: The market ticker (e.g. `'BTC-USD'`).
    - `effective_before_or_at`: If given, fetches funding rates up to and including the given timestamp.
    - `effective_before_or_at_height`: If given, fetches funding rates up to and including the given block height.
    - `limit`: The max. number of candles to retrieve (default: 1000, max: 1000).
    """
    last_block = effective_before_or_at_height or -1
    async def next(last_block: int | None) -> tuple[list[Funding], int | None]:
      if last_block == -1:
        last_block = None
      response = await self.get_historical_funding(
        market,
        effective_before_or_at=effective_before_or_at,
        effective_before_or_at_height=last_block,
        limit=limit,
      )
      historical_funding = response['historicalFunding']
      if not historical_funding:
        return [], None
      else:
        new_last_block = int(historical_funding[-1]['effectiveAtHeight'])
        if new_last_block == last_block:
          return [], None
      
      return historical_funding, new_last_block

    return PaginatedResponse(last_block, next)