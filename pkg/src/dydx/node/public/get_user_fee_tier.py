from dataclasses import dataclass
from decimal import Decimal

from grpc._channel import _InactiveRpcError

from dydx.core import ApiError
from dydx.node.core import PublicNodeMixin

@dataclass
class FeeTier:
  maker: Decimal
  """Maker fee (relative to base fill size, e.g. 0.01 = 1%)"""
  taker: Decimal
  """Taker fee (relative to base fill size, e.g. 0.01 = 1%)"""

@dataclass
class GetUserFeeTier(PublicNodeMixin):
  async def get_user_fee_tier(self, address: str) -> FeeTier:
    """
    Retrieves the perpetual fee tier associated with a specific wallet address, providing information on the user's current fee structure.

    - `address`: The wallet address that owns the account.

    > [dYdX API docs](https://docs.dydx.xyz/node-client/public#get-fee-tiers)
    """
    try:
      r = await self.node_client.get_user_fee_tier(address)
      return FeeTier(
        maker=Decimal(r.tier.maker_fee_ppm) / Decimal('1e6'),
        taker=Decimal(r.tier.taker_fee_ppm) / Decimal('1e6'),
      )
    except _InactiveRpcError as e:
      raise ApiError(e._state.code, e._state.details)