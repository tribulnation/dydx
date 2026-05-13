"""dYdX rewards module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.rewards.params import Params

class Rewards(Params, GrpcEndpoint):
  """dYdX rewards query group."""
