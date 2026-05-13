"""dYdX fee tiers module."""

from typing_extensions import Any

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.feetiers.perpetual_fee_params import PerpetualFeeParams
from dydx.chain.modules.feetiers.user_fee_tier import UserFeeTier
from dydx.chain.modules.feetiers.user_staking_tier import UserStakingTier

class Feetiers(PerpetualFeeParams, UserFeeTier, UserStakingTier, GrpcEndpoint):
  """dYdX fee tiers query group."""

  async def call(self, method: str, **fields: Any) -> Any:
    """Call a fee tiers generated query by RPC name."""
    if method == 'UserFeeTier':
      return await self.user_fee_tier(fields['user'])
    if method == 'UserStakingTier':
      return await self.user_staking_tier(fields['address'])
    raise ValueError(f'Unsupported fee tiers query: {method}')
