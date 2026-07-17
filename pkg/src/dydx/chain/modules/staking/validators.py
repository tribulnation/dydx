"""Cosmos staking validators query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.cosmos.staking import v1beta1 as staking_proto

class Validators(GrpcEndpoint):
  """Staking validators endpoint."""

  @wrap_exceptions
  async def validators(
    self, *, status: str = '', pagination: query_proto.PageRequest | None = None,
  ) -> staking_proto.QueryValidatorsResponse:
    """Query staking validators."""
    request = staking_proto.QueryValidatorsRequest(status=status, pagination=pagination)
    return await staking_proto.QueryStub(self.channel).validators(request)

  def validators_paged(
    self, *, status: str = '', limit: int | None = None,
  ) -> PaginatedResponse[staking_proto.Validator, bytes]:
    """Page through staking validators.

    Args:
      status: Optional validator status filter.
      limit: Optional maximum number of validators per page.

    Returns:
      A paginated response yielding validator pages.
    """
    async def next(key: bytes) -> tuple[list[staking_proto.Validator], bytes | None]:
      """Fetch the next validator page."""
      response = await self.validators(
        status=status,
        pagination=page_request(key, limit=limit),
      )
      return response.validators, next_key(response)

    return PaginatedResponse(b'', next)
