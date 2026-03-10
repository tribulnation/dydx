from typing_extensions import Literal, TypedDict, NotRequired, Any, cast
from dataclasses import dataclass
from decimal import Decimal

from v4_proto.dydxprotocol.clob.tx_pb2 import MsgPlaceOrder
from v4_proto.dydxprotocol.clob.order_pb2 import Order as OrderProto
from v4_proto.cosmos.tx.v1beta1.service_pb2 import BroadcastTxResponse, BroadcastMode
from dydx_v4_client import OrderFlags
from dydx_v4_client.node.market import Market
from dydx_v4_client.indexer.rest.constants import OrderType
from dydx_v4_client.node.builder import TxOptions

from dydx.core import ApiError, SHORT_BLOCK_WINDOW, STATEFUL_ORDER_TIME_WINDOW
from dydx.indexer.types import PerpetualMarket
from dydx.node.core import PrivateNodeMixin

Side = Literal['BUY', 'SELL']
TimeInForce = Literal['GOOD_TIL_TIME', 'IMMEDIATE_OR_CANCEL', 'POST_ONLY', 'FILL_OR_KILL']
ConditionType = Literal['TAKE_PROFIT', 'STOP_LOSS']
Flags = Literal['LONG_TERM', 'SHORT_TERM', 'CONDITIONAL']

class Order(TypedDict):
  side: Side
  size: Decimal
  price: Decimal
  flags: Flags
  time_in_force: NotRequired[TimeInForce]
  good_til_block: NotRequired[int]
  good_til_block_time: NotRequired[int]
  client_metadata: NotRequired[int]
  condition_type: NotRequired[ConditionType]
  conditional_order_trigger_subticks: NotRequired[int]
  client_id: NotRequired[int]
  reduce_only: NotRequired[bool]

def rand_id() -> int:
  import random
  return random.randint(0, 100000000)

def parse_flags(flags: Flags) -> OrderFlags:
  match flags:
    case 'LONG_TERM':
      return OrderFlags.LONG_TERM
    case 'SHORT_TERM':
      return OrderFlags.SHORT_TERM
    case 'CONDITIONAL':
      return OrderFlags.CONDITIONAL

def parse_type(type: Literal['MARKET', 'LIMIT']) -> Any:
  match type:
    case 'MARKET':
      return OrderType.MARKET
    case 'LIMIT':
      return OrderType.LIMIT

def parse_side(side: Side) -> OrderProto.Side:
  match side:
    case 'BUY':
      return OrderProto.Side.SIDE_BUY
    case 'SELL':
      return OrderProto.Side.SIDE_SELL

def parse_tif(tif: TimeInForce | None) -> OrderProto.TimeInForce:
  match tif:
    case 'IMMEDIATE_OR_CANCEL':
      return OrderProto.TimeInForce.TIME_IN_FORCE_IOC
    case 'POST_ONLY':
      return OrderProto.TimeInForce.TIME_IN_FORCE_POST_ONLY
    case 'FILL_OR_KILL':
      return OrderProto.TimeInForce.TIME_IN_FORCE_FILL_OR_KILL
    case _:
      return OrderProto.TimeInForce.TIME_IN_FORCE_UNSPECIFIED

class OrderResponse(TypedDict):
  tx: BroadcastTxResponse
  order: OrderProto

@dataclass
class PlaceOrder(PrivateNodeMixin):

  def build_order(
    self, *, market: PerpetualMarket, order: Order,
    good_til_block: int | None = None, good_til_block_time: int | None = None,
    subaccount: int = 0,
  ):
    mkt = Market(market) # type: ignore
    client_id = order.get('client_id') or rand_id()
    order_id = mkt.order_id(
      address=self.address, subaccount_number=subaccount,
      client_id=client_id, order_flags=parse_flags(order['flags']),
    )
    return OrderProto(
      order_id=order_id,
      side=parse_side(order['side']),
      quantums=mkt.calculate_quantums(float(order['size'])),
      subticks=mkt.calculate_subticks(float(order['price'])),
      good_til_block=good_til_block,
      good_til_block_time=good_til_block_time,
      time_in_force=parse_tif(order.get('time_in_force')),
      reduce_only=order.get('reduce_only') or False,
      client_metadata=order.get('client_metadata'),
      condition_type=order.get('condition_type'),
      conditional_order_trigger_subticks=order.get('conditional_order_trigger_subticks'),
    )

  async def build_order_now(self, market: PerpetualMarket, order: Order, *, subaccount: int = 0):
    if (gtb := order.get('good_til_block')) is None and order['flags'] == 'SHORT_TERM':
      latest_block = await self.node_client.latest_block()
      gtb = latest_block.block.header.height + SHORT_BLOCK_WINDOW

    if (gtbt := order.get('good_til_block_time')) is None and order['flags'] == 'LONG_TERM':
      latest_block = await self.node_client.latest_block()
      gtbt = latest_block.block.header.time.seconds + STATEFUL_ORDER_TIME_WINDOW
      gtb = None

    return self.build_order(market=market, order=order, good_til_block=gtb, good_til_block_time=gtbt, subaccount=subaccount)

  async def place_order(
    self, market: PerpetualMarket, order: Order, *, subaccount: int = 0,
    mode: BroadcastMode = BroadcastMode.BROADCAST_MODE_SYNC, tx_options: TxOptions | None = None,
  ) -> OrderResponse:
    """Place an order.
    
    - `market`: market to place the order on
    - `order`: order to place
    - `subaccount`: subaccount to place the order on

    > [dYdX API docs](https://docs.dydx.xyz/node-client/private#place-order)
    """
    order_proto = await self.build_order_now(market, order, subaccount=subaccount)
    tx: BroadcastTxResponse = await self.node_client.broadcast_message(
      self.wallet, MsgPlaceOrder(order=order_proto), # type: ignore
      mode=mode, tx_options=tx_options
    )
    if tx.tx_response.code != 0:
      raise ApiError(tx.tx_response.code, tx.tx_response, tx.tx_response.raw_log)
    return {
      'tx': tx,
      'order': order_proto,
    }