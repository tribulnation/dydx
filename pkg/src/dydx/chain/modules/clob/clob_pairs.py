"""dYdX CLOB pairs query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import clob as clob_proto

class ClobPairs(GrpcEndpoint):
  """CLOB pairs endpoint."""

  async def clob_pairs(self, *, pagination: query_proto.PageRequest | None = None) -> clob_proto.QueryClobPairAllResponse:
    """Query all CLOB pairs."""
    request = clob_proto.QueryAllClobPairRequest(pagination=pagination)
    return await clob_proto.QueryStub(self.channel).clob_pair_all(request)
