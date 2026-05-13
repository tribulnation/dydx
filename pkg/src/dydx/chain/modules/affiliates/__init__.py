"""dYdX affiliates module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.affiliates.affiliate_info import AffiliateInfo
from dydx.chain.modules.affiliates.referred_by import ReferredBy

class Affiliates(AffiliateInfo, ReferredBy, GrpcEndpoint):
  """dYdX affiliates query group."""
