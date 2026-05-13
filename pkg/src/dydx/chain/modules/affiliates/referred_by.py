"""dYdX referred-by query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.dydxprotocol import affiliates as affiliates_proto

class ReferredBy(GrpcEndpoint):
  """Referred-by endpoint."""

  async def referred_by(self, address: str) -> affiliates_proto.ReferredByResponse:
    """Query the affiliate referrer for an address."""
    return await affiliates_proto.QueryStub(self.channel).referred_by(affiliates_proto.ReferredByRequest(address=address))
