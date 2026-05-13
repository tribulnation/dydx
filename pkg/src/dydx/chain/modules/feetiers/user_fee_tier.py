"""dYdX user fee tier query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.dydxprotocol import feetiers as feetiers_proto

class UserFeeTier(GrpcEndpoint):
  """User fee tier endpoint."""

  async def user_fee_tier(self, user: str) -> feetiers_proto.QueryUserFeeTierResponse:
    """Query the fee tier for a user."""
    return await feetiers_proto.QueryStub(self.channel).user_fee_tier(feetiers_proto.QueryUserFeeTierRequest(user=user))
