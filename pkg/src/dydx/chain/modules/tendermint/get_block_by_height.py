"""Cosmos Tendermint block by height query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.cosmos.base.tendermint import v1beta1 as tendermint_proto

class GetBlockByHeight(GrpcEndpoint):
  """Tendermint block by height endpoint."""

  @wrap_exceptions
  async def get_block_by_height(self, height: int) -> tendermint_proto.GetBlockByHeightResponse:
    """Query a block by height."""
    return await tendermint_proto.ServiceStub(self.channel).get_block_by_height(tendermint_proto.GetBlockByHeightRequest(height=height))
