"""Cosmos staking validators query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.cosmos.staking import v1beta1 as staking_proto

class Validators(GrpcEndpoint):
  """Staking validators endpoint."""

  async def validators(
    self, *, status: str = '', pagination: query_proto.PageRequest | None = None,
  ) -> staking_proto.QueryValidatorsResponse:
    """Query staking validators."""
    request = staking_proto.QueryValidatorsRequest(status=status, pagination=pagination)
    return await staking_proto.QueryStub(self.channel).validators(request)
