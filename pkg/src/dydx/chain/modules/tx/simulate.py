"""Cosmos tx simulation query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.cosmos.tx import v1beta1 as tx_proto

class Simulate(GrpcEndpoint):
  """Transaction simulation endpoint."""

  @wrap_exceptions
  async def simulate(
    self,
    tx_bytes: bytes = b'',
    *,
    tx: tx_proto.Tx | None = None,
  ) -> tx_proto.SimulateResponse:
    """Simulate an encoded or structured transaction."""
    request = tx_proto.SimulateRequest(tx_bytes=tx_bytes, tx=tx)
    return await tx_proto.ServiceStub(self.channel).simulate(request)
