"""dYdX market prices query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import prices as prices_proto

class MarketPrices(GrpcEndpoint):
  """Market prices endpoint."""

  async def market_prices(
    self, *, pagination: query_proto.PageRequest | None = None,
  ) -> prices_proto.QueryAllMarketPricesResponse:
    """Query all market prices."""
    request = prices_proto.QueryAllMarketPricesRequest(pagination=pagination)
    return await prices_proto.QueryStub(self.channel).all_market_prices(request)
