from typing_extensions import AsyncIterable, Sequence
from dataclasses import dataclass
from datetime import datetime

from dydx.core import timestamp as ts, TypedDict
from .core import IndexerMixin, response_parser

class Funding(TypedDict):
  ticker: str
  rate: str
  price: str
  effectiveAtHeight: str
  effectiveAt: str

class HistoricalFunding(TypedDict):
  historicalFunding: list[Funding]

parse_response = response_parser(HistoricalFunding)

@dataclass
class GetHistoricalFunding(IndexerMixin):
  async def get_historical_funding(
    self, market: str, *,
    end: datetime | None = None,
    end_block: int | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> list[Funding]:
    """Retrieves historical funding rates for a specific perpetual market..

    - `market`: The market ticker (e.g. `'BTC-USD'`).
    - `end`: If given, fetches funding rates up to and including the given timestamp.
    - `end_block`: If given, fetches funding rates up to and including the given block height.
    - `limit`: The max. number of candles to retrieve (default: 1000, max: 1000).
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-historical-funding)
    """
    params = {}
    if end is not None:
      params['effectiveBeforeOrAt'] = ts.dump(end)
    if end_block is not None:
      params['effectiveBeforeOrAtHeight'] = end_block
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', f'/v4/historicalFunding/{market}', params=params)
    return parse_response(r, validate=self.validate(validate))['historicalFunding']

  
  async def get_historical_funding_paged(
    self, market: str, *,
    end: datetime | None = None,
    end_block: int | None = None,
    limit: int | None = None,
  ) -> AsyncIterable[Sequence[Funding]]:
    """Retrieves historical funding rates for a specific perpetual market, automatically paginating.

      - `market`: The market ticker (e.g. `'BTC-USD'`).
      - `end`: If given, fetches funding rates up to and including the given timestamp.
      - `end_block`: If given, fetches funding rates up to and including the given block height.
      - `limit`: The max. number of candles to retrieve (default: 1000, max: 1000).
      - `validate`: Whether to validate the response against the expected schema.

      > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-historical-funding)
      """
    last_block = end_block
    while True:
      fs = await self.get_historical_funding(market, end=end, end_block=last_block, limit=limit)
      if not fs:
        break
      new_last_block = int(fs[-1]['effectiveAtHeight'])
      if new_last_block == last_block:
        break
      last_block = new_last_block
      yield fs