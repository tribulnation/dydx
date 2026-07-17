"""dYdX assets query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import assets as assets_proto

class AssetsAll(GrpcEndpoint):
  """Assets list endpoint."""

  @wrap_exceptions
  async def assets(self, *, pagination: query_proto.PageRequest | None = None) -> assets_proto.QueryAllAssetsResponse:
    """Query all assets."""
    request = assets_proto.QueryAllAssetsRequest(pagination=pagination)
    return await assets_proto.QueryStub(self.channel).all_assets(request)

  def assets_paged(self, *, limit: int | None = None) -> PaginatedResponse[assets_proto.Asset, bytes]:
    """Page through dYdX assets.

    Args:
      limit: Optional maximum number of assets per page.

    Returns:
      A paginated response yielding asset pages.
    """
    async def next(key: bytes) -> tuple[list[assets_proto.Asset], bytes | None]:
      """Fetch the next asset page."""
      response = await self.assets(pagination=page_request(key, limit=limit))
      return response.asset, next_key(response)

    return PaginatedResponse(b'', next)
