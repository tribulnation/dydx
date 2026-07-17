"""Cosmos auth accounts query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.auth import v1beta1 as auth_proto
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.google.protobuf import Any

class Accounts(GrpcEndpoint):
  """Auth accounts endpoint."""

  @wrap_exceptions
  async def accounts(self, *, pagination: query_proto.PageRequest | None = None) -> auth_proto.QueryAccountsResponse:
    """Query chain accounts."""
    request = auth_proto.QueryAccountsRequest(pagination=pagination)
    return await auth_proto.QueryStub(self.channel).accounts(request)

  def accounts_paged(self, *, limit: int | None = None) -> PaginatedResponse[Any, bytes]:
    """Page through chain accounts.

    Args:
      limit: Optional maximum number of accounts per page.

    Returns:
      A paginated response yielding account payload pages.
    """
    async def next(key: bytes) -> tuple[list[Any], bytes | None]:
      """Fetch the next account page."""
      response = await self.accounts(pagination=page_request(key, limit=limit))
      return response.accounts, next_key(response)

    return PaginatedResponse(b'', next)
