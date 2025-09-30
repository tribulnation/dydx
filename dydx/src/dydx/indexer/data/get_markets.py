from typing_extensions import Literal, overload
from dataclasses import dataclass

from dydx.core.types import PerpetualMarket
from .core import IndexerMixin, response_parser, Response, TypedDict

class Markets(TypedDict):
  markets: dict[str, PerpetualMarket]

parse_response = response_parser(Markets)

@dataclass
class GetMarkets(IndexerMixin):
  @overload
  async def get_markets(self, market: str | None = None, *, limit: int | None = None, validate: bool | None = None, unsafe: Literal[True] = True) -> Markets:
    ...
  @overload
  async def get_markets(self, market: str | None = None, *, limit: int | None = None, validate: bool | None = None) -> Response[Markets]:
    ...
  async def get_markets(
    self, market: str | None, *, limit: int | None = None, validate: bool | None = None, unsafe: bool = False,
  ) -> Response[Markets] | Markets:
    """Retrieves perpetual markets.

    - `market`: The specific market ticker to retrieve (e.g. `'BTC-USD'`). If not provided, all markets are returned.
    - `limit`: 	Maximum number of asset positions to return in the response.
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-perpetual-markets)
    """
    params = {}
    if market is not None:
      params['market'] = market
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/v4/perpetualMarkets', params=params)
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))

  
  @overload
  async def get_market(self, market: str, *, limit: int | None = None, validate: bool | None = None, unsafe: Literal[True] = True) -> PerpetualMarket:
    ...
  @overload
  async def get_market(self, market: str, *, limit: int | None = None, validate: bool | None = None) -> Response[PerpetualMarket]:
    ...
  async def get_market(
    self, market: str, *, limit: int | None = None, validate: bool | None = None, unsafe: bool = False,
  ) -> Response[PerpetualMarket] | PerpetualMarket:
    """Retrieves perpetual markets.

    - `market`: The specific market ticker to retrieve (e.g. `'BTC-USD'`). If not provided, all markets are returned.
    - `limit`: 	Maximum number of asset positions to return in the response.
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-perpetual-markets)
    """
    r = await self.get_markets(market, limit=limit, validate=validate, unsafe=unsafe)
    if unsafe:
      return r['markets'][market]
    elif r['status'] == 'OK':
      return {
        'status': 'OK',
        'data': r['data']['markets'][market],
      }
    else:
      return r
