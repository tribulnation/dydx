from typing_extensions import AsyncIterable, Sequence, Literal
from dataclasses import dataclass
from datetime import datetime, timedelta

from trading_sdk.market.market_data.candles import PerpCandles, Candle

from dydx.core import timestamp as ts

from .mixin import MarketDataMixin, IndexerClient

Resolution = Literal['1MIN', '5MINS', '15MINS', '30MINS', '1HOUR', '4HOURS', '1DAY']

async def paged_candles(
  client: IndexerClient,
  instrument: str, *,
  start: datetime,
  end: datetime,
  resolution: Resolution,
  limit: int | None = None,
) -> AsyncIterable[Sequence[Candle]]:
  start_iso = ts.dump(start)
  last_time = end
  while True:
    r = await client.markets.get_perpetual_market_candles(
      instrument, resolution, limit=limit,
      start=start_iso, end=ts.dump(last_time)
    )
    candles = r['candles']


@dataclass
class Candles(PerpCandles, MarketDataMixin):
  async def candles(
    self, instrument: str, /, *,
    interval: timedelta,
    start: datetime, end: datetime,
    limit: int | None = None
  ) -> AsyncIterable[Sequence[Candle]]:
    mins = int(interval.total_seconds() // 60)
    async for c in self.inde(instrument, start=start, end=end, resolution=mins):
      yield [
        Candle(
          open=c['open'][i],
          high=c['high'][i],
          low=c['low'][i],
          close=c['close'][i],
          volume=c['volume'][i],
          time=ts.parse(c['ticks'][i]),
        )
        for i in range(len(c['open']))
      ]

  async def perp_candles(self, base: str, quote: str, /, *, interval: timedelta, start: datetime, end: datetime, limit: int | None = None) -> AsyncIterable[Sequence[Candle]]:
    instrument = perp_name(base, quote)
    async for c in self.candles(instrument, interval=interval, start=start, end=end, limit=limit):
      yield c