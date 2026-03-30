from typing_extensions import AsyncIterable, Literal, Sequence
from dataclasses import dataclass
from datetime import datetime

from dydx.core import timestamp as ts
from .api.get_candles import GetCandles, Candle

Resolution = Literal['1MIN', '5MINS', '15MINS', '30MINS', '1HOUR', '4HOURS', '1DAY']

@dataclass
class GetCandlesPaged(GetCandles):
  async def get_candles_paged(
    self,
    market: str,
    resolution: Resolution,
    *,
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
      response = await self.get_candles(
        market,
        resolution=resolution,
        from_iso=start,
        to_iso=last_time,
        limit=limit,
      )
      candles = response['candles']
      if not candles:
        break
      yield candles
      last_time = candles[-1]['startedAt']
