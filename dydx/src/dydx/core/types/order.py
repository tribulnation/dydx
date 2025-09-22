from typing_extensions import NotRequired

from dydx.core import TypedDict
from .enums import OrderSide, OrderStatus, OrderType, TimeInForce

class OrderState(TypedDict):
  """Order Response Object

  > [dYdX API docs](https://docs.dydx.xyz/types/order_response_object)
  """
  id: str
  subaccountId: str
  clientId: str
  clobPairId: str
  side: OrderSide
  size: str
  totalFilled: str
  price: str
  type: OrderType
  status: OrderStatus
  timeInForce: TimeInForce
  reduceOnly: NotRequired[bool|None]
  orderFlags: str
  goodTilBlock: NotRequired[str|None]
  createdAtHeight: str
  clientMetadata: str
  updatedAt: str
  updatedAtHeight: str
  orderRouterAddress: NotRequired[str|None]
  postOnly: NotRequired[bool|None]
  ticker: str
  subaccountNumber: int
