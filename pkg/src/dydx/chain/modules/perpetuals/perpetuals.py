"""dYdX perpetuals query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import perpetuals as perpetuals_proto

class PerpetualsAll(GrpcEndpoint):
  """Perpetuals list endpoint."""

  async def perpetuals(self, *, pagination: query_proto.PageRequest | None = None) -> perpetuals_proto.QueryAllPerpetualsResponse:
    """Query all perpetuals."""
    request = perpetuals_proto.QueryAllPerpetualsRequest(pagination=pagination)
    return await perpetuals_proto.QueryStub(self.channel).all_perpetuals(request)

  def perpetuals_paged(
    self, *, limit: int | None = None,
  ) -> PaginatedResponse[perpetuals_proto.Perpetual, bytes]:
    """Page through all perpetuals.

    Args:
      limit: Optional maximum number of perpetuals per page.

    Returns:
      A paginated response yielding perpetual pages.
    """
    async def next(key: bytes) -> tuple[list[perpetuals_proto.Perpetual], bytes | None]:
      """Fetch the next perpetual page."""
      response = await self.perpetuals(pagination=page_request(key, limit=limit))
      return response.perpetual, next_key(response)

    return PaginatedResponse(b'', next)
