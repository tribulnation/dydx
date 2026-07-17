"""Cosmos staking pool query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.cosmos.staking import v1beta1 as staking_proto

class Pool(GrpcEndpoint):
  """Staking pool endpoint."""

  @wrap_exceptions
  async def pool(self) -> staking_proto.QueryPoolResponse:
    """Query staking pool state."""
    return await staking_proto.QueryStub(self.channel).pool(staking_proto.QueryPoolRequest())
