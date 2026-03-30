from dataclasses import dataclass
from decimal import Decimal

from grpc._channel import _InactiveRpcError

from typed_core.exceptions import ApiError
from dydx.node.core import PublicNodeMixin

@dataclass
class GetPrice(PublicNodeMixin):
  async def get_price(self, id: int):
    """
    Retrieve the current market price for a specified market, identified by its market ID.

    - `id`: The id of the CLOB pair.

    > [dYdX API docs](https://docs.dydx.xyz/node-client/public#get-price)
    """
    try:
      r = await self.node_client.get_price(id)
      return Decimal(r.price) * Decimal(f'1e{r.exponent}')
    except _InactiveRpcError as e:
      raise ApiError(e._state.code, e._state.details)