"""Cosmos Tendermint latest block query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.cosmos.base.tendermint import v1beta1 as tendermint_proto

class GetLatestBlock(GrpcEndpoint):
  """Tendermint latest block endpoint."""

  @wrap_exceptions
  async def get_latest_block(self) -> tendermint_proto.GetLatestBlockResponse:
    """Query the latest block."""
    return await tendermint_proto.ServiceStub(self.channel).get_latest_block(tendermint_proto.GetLatestBlockRequest())
