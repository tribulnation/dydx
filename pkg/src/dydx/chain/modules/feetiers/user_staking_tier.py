"""dYdX user staking tier query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.dydxprotocol import feetiers as feetiers_proto

class UserStakingTier(GrpcEndpoint):
  """User staking tier endpoint."""

  @wrap_exceptions
  async def user_staking_tier(self, address: str) -> feetiers_proto.QueryUserStakingTierResponse:
    """Query the staking fee tier for a user."""
    return await feetiers_proto.QueryStub(self.channel).user_staking_tier(feetiers_proto.QueryUserStakingTierRequest(address=address))
