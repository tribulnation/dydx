"""Cosmos staking module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.staking.delegator_delegations import DelegatorDelegations
from dydx.chain.modules.staking.pool import Pool
from dydx.chain.modules.staking.validators import Validators

class Staking(DelegatorDelegations, Pool, Validators, GrpcEndpoint):
  """Cosmos staking query group."""
