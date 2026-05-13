"""dYdX assets query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import assets as assets_proto

class AssetsAll(GrpcEndpoint):
  """Assets list endpoint."""

  async def assets(self, *, pagination: query_proto.PageRequest | None = None) -> assets_proto.QueryAllAssetsResponse:
    """Query all assets."""
    request = assets_proto.QueryAllAssetsRequest(pagination=pagination)
    return await assets_proto.QueryStub(self.channel).all_assets(request)
