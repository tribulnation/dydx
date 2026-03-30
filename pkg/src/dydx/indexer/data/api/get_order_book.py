from dataclasses import dataclass
from decimal import Decimal
from typing_extensions import TypedDict
from ..core import IndexerMixin, response_parser

class BookEntry(TypedDict):
  price: Decimal
  size: Decimal

class OrderBook(TypedDict):
  bids: list[BookEntry]
  asks: list[BookEntry]

parse_response = response_parser(OrderBook)

@dataclass
class GetOrderBook(IndexerMixin):
  async def get_order_book(
    self,
    market: str,
    validate: bool | None = None
  ) -> OrderBook:
    """
    Retrieve the orderbook for a perpetual market.

    - `market`: Perpetual market ticker.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http#get-perpetual-market-orderbook)
    """
    r = await self.request('GET', f'/v4/orderbooks/perpetualMarket/{market}')
    return parse_response(r, validate=self.validate(validate))

