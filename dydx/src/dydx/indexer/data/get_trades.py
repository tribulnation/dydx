from typing_extensions import Literal, overload, AsyncIterable, Sequence, NotRequired
from dataclasses import dataclass

from dydx.core import TypedDict
from dydx.core.types import OrderSide, OrderType
from .core import IndexerMixin, response_parser, Response

class Trade(TypedDict):
  id: str
  side: OrderSide
  size: str
  price: str
  type: OrderType
  createdAt: str
  createdAtHeight: str

class Trades(TypedDict):
  trades: list[Trade]

parse_response = response_parser(Trades)

@dataclass
class GetTrades(IndexerMixin):
  @overload
  async def get_trades(
    self, market: str, *,
    start_height: int  | None = None,
    limit: int | None = None,
    validate: bool | None = None,
    unsafe: Literal[True] = True,
  ) -> Trades:
    ...
  @overload
  async def get_trades(
    self, market: str, *,
    start_height: int | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> Response[Trades]:
    ...
  async def get_trades(
    self, market: str, *,
    start_height: int | None = None,
    limit: int | None = None,
    validate: bool | None = None,
    unsafe: bool = False,
  ) -> Response[Trades] | Trades:
    """Retrieves trades for a specific perpetual market.

    - `market`: The market ticker (e.g. `'BTC-USD'`).
    - `start_height`: The block height to start retrieving trades from.
    - `limit`: The max. number of trades to retrieve (default: 1000, max: 1000).
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-trades)
    """
    params = {}
    if start_height is not None:
      params['startingBeforeOrAtHeight'] = start_height
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', f'/v4/trades/perpetualMarket/{market}', params=params)
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))
