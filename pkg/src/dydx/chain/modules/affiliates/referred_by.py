"""dYdX referred-by query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.dydxprotocol import affiliates as affiliates_proto

class ReferredBy(GrpcEndpoint):
  """Referred-by endpoint."""

  @wrap_exceptions
  async def referred_by(self, address: str) -> affiliates_proto.ReferredByResponse:
    """Query the affiliate referrer for an address."""
    return await affiliates_proto.QueryStub(self.channel).referred_by(affiliates_proto.ReferredByRequest(address=address))
