"""dYdX rewards params query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.dydxprotocol import rewards as rewards_proto

class Params(GrpcEndpoint):
  """Rewards params endpoint."""

  @wrap_exceptions
  async def params(self) -> rewards_proto.QueryParamsResponse:
    """Query rewards parameters."""
    return await rewards_proto.QueryStub(self.channel).params(rewards_proto.QueryParamsRequest())
