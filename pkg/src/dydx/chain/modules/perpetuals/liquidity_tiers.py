"""dYdX liquidity tiers query."""

from dydx.chain.core import GrpcEndpoint
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
