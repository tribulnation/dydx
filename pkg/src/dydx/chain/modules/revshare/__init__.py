"""dYdX revshare module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.revshare.market_mapper_rev_share_details import MarketMapperRevShareDetails
from dydx.chain.modules.revshare.order_router_rev_share import OrderRouterRevShare

class Revshare(MarketMapperRevShareDetails, OrderRouterRevShare, GrpcEndpoint):
  """dYdX revshare query group."""
