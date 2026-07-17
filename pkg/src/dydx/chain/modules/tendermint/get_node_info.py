"""Cosmos Tendermint node info query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.cosmos.base.tendermint import v1beta1 as tendermint_proto

class GetNodeInfo(GrpcEndpoint):
  """Tendermint node info endpoint."""

  @wrap_exceptions
  async def get_node_info(self) -> tendermint_proto.GetNodeInfoResponse:
    """Query node information."""
    return await tendermint_proto.ServiceStub(self.channel).get_node_info(tendermint_proto.GetNodeInfoRequest())
