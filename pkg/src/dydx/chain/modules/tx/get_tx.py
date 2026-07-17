"""Cosmos tx get transaction query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.cosmos.tx import v1beta1 as tx_proto

class GetTx(GrpcEndpoint):
  """Transaction lookup endpoint."""

  @wrap_exceptions
  async def get_tx(self, hash: str) -> tx_proto.GetTxResponse:
    """Query a transaction by hash."""
    return await tx_proto.ServiceStub(self.channel).get_tx(tx_proto.GetTxRequest(hash=hash))
