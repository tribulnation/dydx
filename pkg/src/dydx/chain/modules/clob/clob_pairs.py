"""dYdX CLOB pairs query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import clob as clob_proto

class ClobPairs(GrpcEndpoint):
  """CLOB pairs endpoint."""

  @wrap_exceptions
  async def clob_pairs(self, *, pagination: query_proto.PageRequest | None = None) -> clob_proto.QueryClobPairAllResponse:
    """Query all CLOB pairs."""
    request = clob_proto.QueryAllClobPairRequest(pagination=pagination)
    return await clob_proto.QueryStub(self.channel).clob_pair_all(request)

  def clob_pairs_paged(self, *, limit: int | None = None) -> PaginatedResponse[clob_proto.ClobPair, bytes]:
    """Page through all CLOB pairs.

    Args:
      limit: Optional maximum number of CLOB pairs per page.

    Returns:
      A paginated response yielding CLOB pair pages.
    """
    async def next(key: bytes) -> tuple[list[clob_proto.ClobPair], bytes | None]:
      """Fetch the next CLOB pair page."""
      response = await self.clob_pairs(pagination=page_request(key, limit=limit))
      return response.clob_pair, next_key(response)

    return PaginatedResponse(b'', next)
