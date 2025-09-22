from typing_extensions import Literal, overload, AsyncIterable, Sequence
from dataclasses import dataclass
from datetime import datetime

from dydx.core import timestamp as ts, TypedDict
from .core import IndexerMixin, response_parser, Response

Resolution = Literal['1MIN', '5MINS', '15MINS', '30MINS', '1HOUR', '4HOURS', '1DAY']

class Candle(TypedDict):
  startedAt: str
  ticker: str
  resolution: Resolution
  low: str
  high: str
  open: str
  close: str
  baseTokenVolume: str
  usdVolume: str
  trades: int
  startingOpenInterest: str
  orderbookMidPriceOpen: str
  orderbookMidPriceClose: str

class GetCandles(TypedDict):
  candles: list[Candle]

parse_response = response_parser(GetCandles)

@dataclass
class GetCandles(IndexerMixin):
  @overload
  async def get_candles(
    self, market: str, resolution: Resolution, *,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int | None = None,
    validate: bool = True,
    unsafe: Literal[True] = True,
  ) -> GetCandles:
    ...
  @overload
  async def get_candles(
    self, market: str, resolution: Resolution, *,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int | None = None,
    validate: bool = True,
  ) -> Response[GetCandles]:
    ...
  async def get_candles(
    self, market: str, resolution: Resolution, *,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int | None = None,
    validate: bool = True,
    unsafe: bool = False,
  ) -> Response[GetCandles] | GetCandles:
    """Retrieves candle data for a specific perpetual market.

    - `market`: The market ticker (e.g. `'BTC-USD'`).
    - `resolution`: The resolution of the candles.
    - `start`: If given, fetches candles starting from the given timestamp.
    - `end`: If given, fetches candles up to the given timestamp.
    - `limit`: The max. number of candles to retrieve (default: 1000, max: 1000).
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-candles)
    """
    params = {'resolution': resolution}
    if start is not None:
      params['fromISO'] = ts.dump(start)
    if end is not None:
      params['toISO'] = ts.dump(end)
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', f'/v4/candles/perpetualMarkets/{market}', params=params)
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))

  
  async def get_candles_paged(
    self, market: str, resolution: Resolution, *,
    start: datetime | None = None,
    end: datetime | None = None,
    limit: int | None = None,
  ) -> AsyncIterable[Sequence[Candle]]:
    """Retrieves candle data for a specific perpetual market, paging as needed.

    - `market`: The market ticker (e.g. `'BTC-USD'`).
    - `resolution`: The resolution of the candles.
    - `start`: If given, fetches candles starting from the given timestamp.
    - `end`: If given, fetches candles up to and including the given timestamp.
    - `limit`: The max. number of candles to retrieve per request (default: 1000, max: 1000).
    """
    last_time = end
    while True:
      r = await self.get_candles(market, resolution, start=start, end=last_time, limit=limit, unsafe=True)
      if not r['candles']:
        break
      yield r['candles']
      last_time = ts.parse(r['candles'][-1]['startedAt'])