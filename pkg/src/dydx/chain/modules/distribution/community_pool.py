"""Cosmos distribution community pool query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.cosmos.distribution import v1beta1 as distribution_proto

class CommunityPool(GrpcEndpoint):
  """Community pool endpoint."""

  @wrap_exceptions
  async def community_pool(self) -> distribution_proto.QueryCommunityPoolResponse:
    """Query distribution community pool funds."""
    return await distribution_proto.QueryStub(self.channel).community_pool(distribution_proto.QueryCommunityPoolRequest())
