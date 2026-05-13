"""dYdX CLOB leverage query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.dydxprotocol import clob as clob_proto

class Leverage(GrpcEndpoint):
  """CLOB leverage endpoint."""

  async def leverage(self, *, owner: str, number: int = 0) -> clob_proto.QueryLeverageResponse:
    """Query leverage info for a subaccount."""
    return await clob_proto.QueryStub(self.channel).leverage(clob_proto.QueryLeverageRequest(owner=owner, number=number))
