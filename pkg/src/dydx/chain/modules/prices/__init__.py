"""dYdX prices module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.prices.market_param import MarketParam
from dydx.chain.modules.prices.market_price import MarketPrice
from dydx.chain.modules.prices.market_prices import MarketPrices

class Prices(MarketParam, MarketPrice, MarketPrices, GrpcEndpoint):
  """dYdX prices query group."""
