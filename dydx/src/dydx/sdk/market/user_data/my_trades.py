from typing_extensions import AsyncIterable, Sequence
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal

from trading_sdk.market.user_data.my_trades import (
  PerpMyTrades, Trade
)

from dydx.core import timestamp as ts
from dydx.sdk.core import UserDataMixin, wrap_exceptions, perp_name

@dataclass
class MyTrades(UserDataMixin, PerpMyTrades):

  @wrap_exceptions
  async def my_trades(
    self, instrument: str, /, *,
    start: datetime | None = None, end: datetime | None = None
  ) -> AsyncIterable[Sequence[Trade]]:

    if start is not None:
      start = start.astimezone()
    if end is not None:
      end = end.astimezone()
      
    def within(t: datetime) -> bool:
      after = start is None or t >= start
      before = end is None or t <= end
      return after and before

    async for fills in self.indexer_data.get_fills_paged(
      self.address, subaccount=self.subaccount, ticker=instrument, end=end,
    ):
      trades = [
        Trade(
          id=f['id'],
          price=Decimal(f['price']),
          qty=Decimal(f['size']),
          time=t,
          side=f['side'],
          maker=f['liquidity'] == 'MAKER',
        )
        for f in fills
          if within(t := ts.parse(f['createdAt']))
      ]
      if trades:
        yield trades

  async def perp_my_trades(self, base: str, quote: str, /, *, start: datetime | None = None, end: datetime | None = None) -> AsyncIterable[Sequence[Trade]]:
    instrument = perp_name(base, quote)
    async for trades in self.my_trades(instrument, start=start, end=end):
      yield trades