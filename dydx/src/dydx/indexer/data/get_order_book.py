from typing_extensions import overload, Literal
from dataclasses import dataclass

from dydx.core import TypedDict
from .core import IndexerMixin, response_parser, Response

class BookEntry(TypedDict):
  price: str
  size: str

class Book(TypedDict):
  bids: list[BookEntry]
  asks: list[BookEntry]

parse_response = response_parser(Book)

@dataclass
class GetOrderBook(IndexerMixin):
  @overload
  async def get_order_book(self, market: str, /, *, unsafe: Literal[True] = True, validate: bool | None = None) -> Book:
    ...
  @overload
  async def get_order_book(self, market: str, /, *, validate: bool | None = None) -> Response[Book]:
    ...
  async def get_order_book(
    self, market: str, /, *, unsafe: bool = False, validate: bool | None = None
  ) -> Response[Book] | Book:
    """Retrieves the orderbook for a specific perpetual market.
    
    - `market`: The market ticker (e.g. `'BTC-USD'`).
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-perpetual-market-orderbook)
    """
    r = await self.request('GET', f'/v4/orderbooks/perpetualMarket/{market}')
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))