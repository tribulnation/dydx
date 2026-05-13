"""dYdX subaccounts query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import subaccounts as subaccounts_proto

class SubaccountsAll(GrpcEndpoint):
  """Subaccounts list endpoint."""

  async def subaccounts(self, *, pagination: query_proto.PageRequest | None = None) -> subaccounts_proto.QuerySubaccountAllResponse:
    """Query all subaccounts."""
    request = subaccounts_proto.QueryAllSubaccountRequest(pagination=pagination)
    return await subaccounts_proto.QueryStub(self.channel).subaccount_all(request)

  def subaccounts_paged(
    self, *, limit: int | None = None,
  ) -> PaginatedResponse[subaccounts_proto.Subaccount, bytes]:
    """Page through all subaccounts.

    Args:
      limit: Optional maximum number of subaccounts per page.

    Returns:
      A paginated response yielding subaccount pages.
    """
    async def next(key: bytes) -> tuple[list[subaccounts_proto.Subaccount], bytes | None]:
      """Fetch the next subaccount page."""
      response = await self.subaccounts(pagination=page_request(key, limit=limit))
      return response.subaccount, next_key(response)

    return PaginatedResponse(b'', next)
