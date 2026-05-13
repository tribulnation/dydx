"""dYdX market price query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.dydxprotocol import prices as prices_proto

class MarketPrice(GrpcEndpoint):
  """Market price endpoint."""

  async def market_price(self, id: int) -> prices_proto.QueryMarketPriceResponse:
    """Query a market price by id."""
    return await prices_proto.QueryStub(self.channel).market_price(prices_proto.QueryMarketPriceRequest(id=id))
