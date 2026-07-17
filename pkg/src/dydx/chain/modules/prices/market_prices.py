"""dYdX market prices query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import prices as prices_proto

class MarketPrices(GrpcEndpoint):
  """Market prices endpoint."""

  @wrap_exceptions
  async def market_prices(
    self, *, pagination: query_proto.PageRequest | None = None,
  ) -> prices_proto.QueryAllMarketPricesResponse:
    """Query all market prices."""
    request = prices_proto.QueryAllMarketPricesRequest(pagination=pagination)
    return await prices_proto.QueryStub(self.channel).all_market_prices(request)

  def market_prices_paged(
    self, *, limit: int | None = None,
  ) -> PaginatedResponse[prices_proto.MarketPrice, bytes]:
    """Page through all market prices.

    Args:
      limit: Optional maximum number of market prices per page.

    Returns:
      A paginated response yielding market price pages.
    """
    async def next(key: bytes) -> tuple[list[prices_proto.MarketPrice], bytes | None]:
      """Fetch the next market price page."""
      response = await self.market_prices(pagination=page_request(key, limit=limit))
      return response.market_prices, next_key(response)

    return PaginatedResponse(b'', next)
