"""Cosmos distribution module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.distribution.community_pool import CommunityPool
from dydx.chain.modules.distribution.delegation_rewards import DelegationRewards
from dydx.chain.modules.distribution.delegation_total_rewards import DelegationTotalRewards

class Distribution(CommunityPool, DelegationRewards, DelegationTotalRewards, GrpcEndpoint):
  """Cosmos distribution query group."""
