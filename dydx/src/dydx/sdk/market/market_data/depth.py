from dataclasses import dataclass
from decimal import Decimal

from trading_sdk.market.market_data.depth import PerpDepth, Book

from dydx.sdk.core import MarketDataMixin, wrap_exceptions, perp_name

@dataclass
class Depth(MarketDataMixin, PerpDepth):
  @wrap_exceptions
  async def depth(self, instrument: str, /, *, limit: int | None = None) -> Book:
    book = await self.indexer_data.get_order_book(instrument, unsafe=True)
    return Book(
      asks=[Book.Entry(
        price=Decimal(p['price']),
        qty=Decimal(p['size'])
      ) for p in book['asks'][:limit]],
      bids=[Book.Entry(
        price=Decimal(p['price']),
        qty=Decimal(p['size'])
      ) for p in book['bids'][:limit]],
    )

  async def perp_depth(self, base: str, quote: str, /, *, limit: int | None = None) -> Book:
    instrument = perp_name(base, quote)
    return await self.depth(instrument, limit=limit)