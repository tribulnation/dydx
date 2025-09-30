from typing_extensions import AsyncIterable, Sequence
from dataclasses import dataclass
from datetime import timedelta, datetime
from decimal import Decimal

from trading_sdk.market.market_data.candles import PerpCandles, Candle

from dydx.core import timestamp as ts
from dydx.sdk.core import MarketDataMixin, wrap_exceptions, perp_name
from dydx.indexer.data.get_candles import Resolution

def parse_interval(dt: timedelta) -> Resolution:
  if dt < timedelta(minutes=5):
    return '1MIN'
  elif dt < timedelta(minutes=15):
    return '5MINS'
  elif dt < timedelta(minutes=30):
    return '15MINS'
  elif dt < timedelta(hours=1):
    return '30MINS'
  elif dt < timedelta(hours=4):
    return '1HOUR'
  else:
    return '1DAY'
  
@dataclass
class Candles(MarketDataMixin, PerpCandles):
  @wrap_exceptions
  async def candles(
    self, instrument: str, /, *,
    interval: timedelta, start: datetime, end: datetime,
    limit: int | None = None
  ) -> AsyncIterable[Sequence[Candle]]:
    async for chunk in self.indexer_data.get_candles_paged(instrument, parse_interval(interval), start=start, end=end, limit=limit):
      yield [
        Candle(
          open=Decimal(c['open']),
          high=Decimal(c['high']),
          low=Decimal(c['low']),
          close=Decimal(c['close']),
          volume=Decimal(c['baseTokenVolume']),
          quote_volume=Decimal(c['usdVolume']),
          time=ts.parse(c['startedAt']).astimezone().replace(tzinfo=None)
        )
        for c in chunk
      ]

  async def perp_candles(self, base: str, quote: str, /, *, interval: timedelta, start: datetime, end: datetime, limit: int | None = None) -> AsyncIterable[Sequence[Candle]]:
    instrument = perp_name(base, quote)
    async for chunk in self.candles(instrument, interval=interval, start=start, end=end, limit=limit):
      yield chunk