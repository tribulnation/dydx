"""dYdX liquidity tiers query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import perpetuals as perpetuals_proto

class LiquidityTiers(GrpcEndpoint):
  """Liquidity tiers endpoint."""

  async def liquidity_tiers(
    self, *, pagination: query_proto.PageRequest | None = None,
  ) -> perpetuals_proto.QueryAllLiquidityTiersResponse:
    """Query all liquidity tiers."""
    request = perpetuals_proto.QueryAllLiquidityTiersRequest(pagination=pagination)
    return await perpetuals_proto.QueryStub(self.channel).all_liquidity_tiers(request)

  def liquidity_tiers_paged(
    self, *, limit: int | None = None,
  ) -> PaginatedResponse[perpetuals_proto.LiquidityTier, bytes]:
    """Page through all liquidity tiers.

    Args:
      limit: Optional maximum number of liquidity tiers per page.

    Returns:
      A paginated response yielding liquidity tier pages.
    """
    async def next(key: bytes) -> tuple[list[perpetuals_proto.LiquidityTier], bytes | None]:
      """Fetch the next liquidity tier page."""
      response = await self.liquidity_tiers(pagination=page_request(key, limit=limit))
      return response.liquidity_tiers, next_key(response)

    return PaginatedResponse(b'', next)
