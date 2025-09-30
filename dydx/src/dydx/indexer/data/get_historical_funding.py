from typing_extensions import Literal, overload, AsyncIterable, Sequence
from dataclasses import dataclass
from datetime import datetime

from dydx.core import timestamp as ts, TypedDict
from .core import IndexerMixin, response_parser, Response

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
  @overload
  async def get_historical_funding(
    self, market: str, *,
    end: datetime | None = None,
    end_block: int | None = None,
    limit: int | None = None,
    validate: bool | None = None,
    unsafe: Literal[True] = True,
  ) -> HistoricalFunding:
    ...
  @overload
  async def get_historical_funding(
    self, market: str, *,
    end: datetime | None = None,
    end_block: int | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> Response[HistoricalFunding]:
    ...
  async def get_historical_funding(
    self, market: str, *,
    end: datetime | None = None,
    end_block: int | None = None,
    limit: int | None = None,
    validate: bool | None = None,
    unsafe: bool = False,
  ) -> Response[HistoricalFunding] | HistoricalFunding:
    """Retrieves historical funding rates for a specific perpetual market..

    - `market`: The market ticker (e.g. `'BTC-USD'`).
    - `end`: If given, fetches funding rates up to and including the given timestamp.
    - `end_block`: If given, fetches funding rates up to and including the given block height.
    - `limit`: The max. number of candles to retrieve (default: 1000, max: 1000).
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

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
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))

  
  async def get_historical_funding_paged(
    self, market: str, *,
    end: datetime | None = None,
    end_block: int | None = None,
    limit: int | None = None,
  ) -> AsyncIterable[Sequence[Funding]]:
    last_block = end_block
    while True:
      r = await self.get_historical_funding(market, end=end, end_block=last_block, limit=limit, unsafe=True)
      fs = r['historicalFunding']
      if not fs:
        break
      new_last_block = int(fs[-1]['effectiveAtHeight'])
      if new_last_block == last_block:
        break
      last_block = new_last_block
      yield fs