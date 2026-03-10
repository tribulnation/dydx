from dataclasses import dataclass

from dydx.core import TypedDict
from dydx.indexer.types import PerpetualMarket
from .core import IndexerMixin, response_parser

class Markets(TypedDict):
  markets: dict[str, PerpetualMarket]

parse_response = response_parser(Markets)

@dataclass
class GetMarkets(IndexerMixin):
  async def get_markets(
    self, market: str | None = None, *, limit: int | None = None, validate: bool | None = None,
  ) -> dict[str, PerpetualMarket]:
    """Retrieves perpetual markets.

    - `market`: The specific market ticker to retrieve (e.g. `'BTC-USD'`). If not provided, all markets are returned.
    - `limit`: 	Maximum number of asset positions to return in the response.
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-perpetual-markets)
    """
    params = {}
    if market is not None:
      params['market'] = market
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/v4/perpetualMarkets', params=params)
    return parse_response(r, validate=self.validate(validate))['markets']

  
  async def get_market(
    self, market: str, *, validate: bool | None = None,
  ) -> PerpetualMarket:
    """Retrieves perpetual markets.

    - `market`: The specific market ticker to retrieve (e.g. `'BTC-USD'`). If not provided, all markets are returned.
    - `limit`: 	Maximum number of asset positions to return in the response.
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-perpetual-markets)
    """
    r = await self.get_markets(market, limit=1, validate=validate)
    return r[market]
