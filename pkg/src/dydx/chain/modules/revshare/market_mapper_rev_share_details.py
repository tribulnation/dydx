"""dYdX market mapper revshare details query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.dydxprotocol import revshare as revshare_proto

class MarketMapperRevShareDetails(GrpcEndpoint):
  """Market mapper revshare details endpoint."""

  @wrap_exceptions
  async def market_mapper_rev_share_details(self, market_id: int) -> revshare_proto.QueryMarketMapperRevShareDetailsResponse:
    """Query market mapper revenue-share details."""
    return await revshare_proto.QueryStub(self.channel).market_mapper_rev_share_details(
      revshare_proto.QueryMarketMapperRevShareDetails(market_id=market_id)
    )
