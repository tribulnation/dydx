"""Cosmos staking delegator delegations query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.cosmos.staking import v1beta1 as staking_proto

class DelegatorUnbondingDelegations(GrpcEndpoint):
  """Delegator delegations endpoint."""

  @wrap_exceptions
  async def delegator_unbonding_delegations(
    self, delegator_addr: str, *, pagination: query_proto.PageRequest | None = None,
  ) -> staking_proto.QueryDelegatorUnbondingDelegationsResponse:
    """Query unbonding delegations for a delegator.
    
    Args:
      delegator_addr: Delegator account address.
      pagination: Optional pagination request.
    """
    request = staking_proto.QueryDelegatorUnbondingDelegationsRequest(
      delegator_addr=delegator_addr,
      pagination=pagination,
    )
    return await staking_proto.QueryStub(self.channel).delegator_unbonding_delegations(request)

  def delegator_unbonding_delegations_paged(
    self, delegator_addr: str, *, limit: int | None = None,
  ) -> PaginatedResponse[staking_proto.UnbondingDelegation, bytes]:
    """Page through unbonding delegations for a delegator.

    Args:
      delegator_addr: Delegator account address.
      limit: Optional maximum number of delegations per page.

    Returns:
      A paginated response yielding delegation pages.
    """
    async def next(key: bytes) -> tuple[list[staking_proto.UnbondingDelegation], bytes | None]:
      """Fetch the next delegation page."""
      response = await self.delegator_unbonding_delegations(
        delegator_addr,
        pagination=page_request(key, limit=limit),
      )
      return response.unbonding_responses, next_key(response)

    return PaginatedResponse(b'', next)
