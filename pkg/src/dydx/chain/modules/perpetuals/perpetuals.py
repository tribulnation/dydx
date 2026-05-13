"""dYdX perpetuals query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import perpetuals as perpetuals_proto

class PerpetualsAll(GrpcEndpoint):
  """Perpetuals list endpoint."""

  async def perpetuals(self, *, pagination: query_proto.PageRequest | None = None) -> perpetuals_proto.QueryAllPerpetualsResponse:
    """Query all perpetuals."""
    request = perpetuals_proto.QueryAllPerpetualsRequest(pagination=pagination)
    return await perpetuals_proto.QueryStub(self.channel).all_perpetuals(request)
