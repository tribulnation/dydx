"""dYdX perpetual fee params query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.dydxprotocol import feetiers as feetiers_proto

class PerpetualFeeParams(GrpcEndpoint):
  """Perpetual fee params endpoint."""

  async def perpetual_fee_params(self) -> feetiers_proto.QueryPerpetualFeeParamsResponse:
    """Query perpetual fee parameters."""
    return await feetiers_proto.QueryStub(self.channel).perpetual_fee_params(feetiers_proto.QueryPerpetualFeeParamsRequest())
