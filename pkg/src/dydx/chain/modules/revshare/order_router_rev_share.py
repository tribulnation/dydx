"""dYdX order router revshare query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.dydxprotocol import revshare as revshare_proto

class OrderRouterRevShare(GrpcEndpoint):
  """Order router revshare endpoint."""

  async def order_router_rev_share(self, address: str) -> revshare_proto.QueryOrderRouterRevShareResponse:
    """Query order router revenue-share state."""
    return await revshare_proto.QueryStub(self.channel).order_router_rev_share(revshare_proto.QueryOrderRouterRevShare(address=address))
