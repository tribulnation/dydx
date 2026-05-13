"""dYdX market param query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.dydxprotocol import prices as prices_proto

class MarketParam(GrpcEndpoint):
  """Market param endpoint."""

  async def market_param(self, id: int) -> prices_proto.QueryMarketParamResponse:
    """Query a market parameter by id."""
    return await prices_proto.QueryStub(self.channel).market_param(prices_proto.QueryMarketParamRequest(id=id))
