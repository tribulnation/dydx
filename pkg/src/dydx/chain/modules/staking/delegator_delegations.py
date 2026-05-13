"""Cosmos staking delegator delegations query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.cosmos.staking import v1beta1 as staking_proto

class DelegatorDelegations(GrpcEndpoint):
  """Delegator delegations endpoint."""

  async def delegator_delegations(
    self, delegator_addr: str, *, pagination: query_proto.PageRequest | None = None,
  ) -> staking_proto.QueryDelegatorDelegationsResponse:
    """Query delegations for a delegator."""
    request = staking_proto.QueryDelegatorDelegationsRequest(
      delegator_addr=delegator_addr,
      pagination=pagination,
    )
    return await staking_proto.QueryStub(self.channel).delegator_delegations(request)
