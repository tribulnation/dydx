"""dYdX perpetuals module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.perpetuals.liquidity_tiers import LiquidityTiers
from dydx.chain.modules.perpetuals.perpetual import Perpetual
from dydx.chain.modules.perpetuals.perpetuals import PerpetualsAll

class Perpetuals(LiquidityTiers, Perpetual, PerpetualsAll, GrpcEndpoint):
  """dYdX perpetuals query group."""
