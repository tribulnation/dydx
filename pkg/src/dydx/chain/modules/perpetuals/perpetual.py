"""dYdX perpetual query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.dydxprotocol import perpetuals as perpetuals_proto

class Perpetual(GrpcEndpoint):
  """Perpetual endpoint."""

  @wrap_exceptions
  async def perpetual(self, id: int) -> perpetuals_proto.QueryPerpetualResponse:
    """Query a perpetual by id."""
    return await perpetuals_proto.QueryStub(self.channel).perpetual(perpetuals_proto.QueryPerpetualRequest(id=id))
