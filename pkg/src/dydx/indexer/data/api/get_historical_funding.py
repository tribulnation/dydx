from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from dydx.core import timestamp as ts
from typing_extensions import TypedDict
from ..core import IndexerMixin, response_parser

class Funding(TypedDict):
  ticker: str
  rate: Decimal
  price: Decimal
  effectiveAt: datetime
  effectiveAtHeight: str

class HistoricalFundingResponse(TypedDict):
  historicalFunding: list[Funding]

parse_response = response_parser(HistoricalFundingResponse)

@dataclass
class GetHistoricalFunding(IndexerMixin):
  async def get_historical_funding(
    self,
    market: str,
    *,
    effective_before_or_at: datetime | None = None,
    effective_before_or_at_height: int | None = None,
    limit: int | None = None,
    validate: bool | None = None
  ) -> HistoricalFundingResponse:
    """
    Retrieve historical funding data for a perpetual market.

    - `market`: Perpetual market ticker.
    - `effective_before_or_at`: Latest effective timestamp to include.
    - `effective_before_or_at_height`: Latest effective block height to include.
    - `limit`: Maximum number of funding entries to return.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http#get-historical-funding)
    """
    params: dict[str, object] = {}
    if effective_before_or_at is not None:
      params['effectiveBeforeOrAt'] = ts.dump(effective_before_or_at)
    if effective_before_or_at_height is not None:
      params['effectiveBeforeOrAtHeight'] = effective_before_or_at_height
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', f'/v4/historicalFunding/{market}', params=params)
    return parse_response(r, validate=self.validate(validate))

