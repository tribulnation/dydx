"""Cosmos Tendermint validator set by height query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.cosmos.base.tendermint import v1beta1 as tendermint_proto

class GetValidatorSetByHeight(GrpcEndpoint):
  """Tendermint validator set by height endpoint."""

  @wrap_exceptions
  async def get_validator_set_by_height(
    self, height: int, *, pagination: query_proto.PageRequest | None = None,
  ) -> tendermint_proto.GetValidatorSetByHeightResponse:
    """Query a validator set by height."""
    request = tendermint_proto.GetValidatorSetByHeightRequest(height=height, pagination=pagination)
    return await tendermint_proto.ServiceStub(self.channel).get_validator_set_by_height(request)

  def get_validator_set_by_height_paged(
    self, height: int, *, limit: int | None = None,
  ) -> PaginatedResponse[tendermint_proto.Validator, bytes]:
    """Page through a validator set by height.

    Args:
      height: Block height to query.
      limit: Optional maximum number of validators per page.

    Returns:
      A paginated response yielding validator pages.
    """
    async def next(key: bytes) -> tuple[list[tendermint_proto.Validator], bytes | None]:
      """Fetch the next validator-set page for the height."""
      response = await self.get_validator_set_by_height(
        height,
        pagination=page_request(key, limit=limit),
      )
      return response.validators, next_key(response)

    return PaginatedResponse(b'', next)
