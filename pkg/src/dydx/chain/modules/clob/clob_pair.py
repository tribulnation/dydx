"""dYdX CLOB pair query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.dydxprotocol import clob as clob_proto

class ClobPair(GrpcEndpoint):
  """CLOB pair endpoint."""

  @wrap_exceptions
  async def clob_pair(self, id: int) -> clob_proto.QueryClobPairResponse:
    """Query a CLOB pair by id."""
    return await clob_proto.QueryStub(self.channel).clob_pair(clob_proto.QueryGetClobPairRequest(id=id))
