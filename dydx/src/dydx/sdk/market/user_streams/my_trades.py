from typing_extensions import AsyncIterable
from dataclasses import dataclass
from decimal import Decimal

from trading_sdk.market.user_streams.my_trades import (
  PerpMyTrades, Trade
)

from dydx.core import timestamp as ts
from dydx.sdk.core import UserStreamsMixin, wrap_exceptions, perp_name

@dataclass
class MyTrades(UserStreamsMixin, PerpMyTrades):

  @wrap_exceptions
  async def my_trades(self, instrument: str, /) -> AsyncIterable[Trade]:
    _, stream = await self.indexer_streams.subaccounts(self.address, subaccount=self.subaccount)
    async for log in stream:
      if (fills := log.get('fills')):
        for fill in fills:
          if fill['ticker'] == instrument:
            yield Trade(
              id=fill['id'],
              price=Decimal(fill['price']),
              qty=Decimal(fill['size']),
              time=ts.parse(fill['createdAt']),
              side=fill['side'],
              maker=fill['liquidity'] == 'MAKER',
            )

  async def perp_my_trades(self, base: str, quote: str, /) -> AsyncIterable[Trade]:
    instrument = perp_name(base, quote)
    async for trade in self.my_trades(instrument):
      yield trade
