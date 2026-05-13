"""dYdX subaccounts module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.subaccounts.collateral_pool_address import CollateralPoolAddress
from dydx.chain.modules.subaccounts.subaccount import Subaccount
from dydx.chain.modules.subaccounts.subaccounts import SubaccountsAll

class Subaccounts(CollateralPoolAddress, Subaccount, SubaccountsAll, GrpcEndpoint):
  """dYdX subaccounts query group."""
