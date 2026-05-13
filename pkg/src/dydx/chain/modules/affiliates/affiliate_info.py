"""dYdX affiliate info query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.dydxprotocol import affiliates as affiliates_proto

class AffiliateInfo(GrpcEndpoint):
  """Affiliate info endpoint."""

  async def affiliate_info(self, address: str) -> affiliates_proto.AffiliateInfoResponse:
    """Query affiliate info for an address."""
    return await affiliates_proto.QueryStub(self.channel).affiliate_info(affiliates_proto.AffiliateInfoRequest(address=address))
