"""dYdX assets module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.assets.asset import Asset
from dydx.chain.modules.assets.assets import AssetsAll

class Assets(Asset, AssetsAll, GrpcEndpoint):
  """dYdX assets query group."""
