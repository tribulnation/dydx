"""dYdX collateral pool address query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.dydxprotocol import subaccounts as subaccounts_proto

class CollateralPoolAddress(GrpcEndpoint):
  """Collateral pool address endpoint."""

  async def collateral_pool_address(self, perpetual_id: int) -> subaccounts_proto.QueryCollateralPoolAddressResponse:
    """Query the collateral pool address for a perpetual."""
    return await subaccounts_proto.QueryStub(self.channel).collateral_pool_address(
      subaccounts_proto.QueryCollateralPoolAddressRequest(perpetual_id=perpetual_id)
    )
