from dataclasses import dataclass

from .api.get_markets import GetMarkets, PerpetualMarket


@dataclass
class GetMarket(GetMarkets):
  async def get_market(
    self,
    market: str,
    *,
    validate: bool | None = None,
  ) -> PerpetualMarket:
    """Retrieves a single perpetual market by ticker."""
    response = await self.get_markets(market=market, limit=1, validate=validate)
    return response['markets'][market] if 'markets' in response else response[market]
