from typing_extensions import Literal, TypedDict, NotRequired
from dataclasses import dataclass
from decimal import Decimal

from v4_proto.dydxprotocol.clob.order_pb2 import Order as OrderProto
from v4_proto.cosmos.tx.v1beta1.service_pb2 import BroadcastTxResponse
from dydx_v4_client import OrderFlags
from dydx_v4_client.node.market import Market
from dydx_v4_client.indexer.rest.constants import OrderType

from dydx.core import ApiError
from dydx.core.types import PerpetualMarket
from dydx.node.private.core import PrivateNodeMixin

Side = Literal['BUY', 'SELL']
TimeInForce = Literal['GOOD_TIL_TIME', 'IMMEDIATE_OR_CANCEL', 'POST_ONLY', 'FILL_OR_KILL']
ConditionType = Literal['TAKE_PROFIT', 'STOP_LOSS']
Flags = Literal['LONG_TERM', 'SHORT_TERM', 'CONDITIONAL']

class BaseOrder(TypedDict):
  side: Side
  size: Decimal
  flags: Flags
  reduce_only: NotRequired[bool]
  time_in_force: NotRequired[TimeInForce]
  good_til_block: NotRequired[int]
  good_til_block_time: NotRequired[int]
  client_metadata: NotRequired[int]
  condition_type: NotRequired[ConditionType]
  conditional_order_trigger_subticks: NotRequired[int]
  client_id: NotRequired[int]

class MarketOrder(BaseOrder):
  type: Literal['MARKET']

class LimitOrder(BaseOrder):
  type: Literal['LIMIT']
  price: Decimal

Order = MarketOrder | LimitOrder

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

def parse_type(type: Literal['MARKET', 'LIMIT']) -> OrderType:
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

def default_gtb(flags: Flags) -> int:
  match flags:
    case 'LONG_TERM':
      return 200
    case 'SHORT_TERM':
      return 20
    case 'CONDITIONAL':
      return 0

class OrderResponse(TypedDict):
  tx: BroadcastTxResponse
  order: OrderProto

@dataclass
class PlaceOrder(PrivateNodeMixin):

  def build_order(
    self, *, market: PerpetualMarket, order: Order,
    good_til_block: int | None = None, good_til_block_time: int | None = None,
  ):
    mkt = Market(market)
    client_id = order.get('client_id') or rand_id()
    order_id = mkt.order_id(
      self.address, 0, client_id,
      order_flags=parse_flags(order['flags'])
    )
    return mkt.order(
      order_id=order_id,
      order_type=parse_type(order['type']),
      side=parse_side(order['side']),
      size=order['size'],
      price=order.get('price', 0),
      time_in_force=parse_tif(order.get('time_in_force')),
      reduce_only=order.get('reduce_only', False),
      post_only=order.get('post_only', False),
      good_til_block=good_til_block,
      good_til_block_time=good_til_block_time,
    )

  async def build_order_now(self, market: PerpetualMarket, order: Order):
    if (gtb := order.get('good_til_block')) is None:
      latest_block = await self.node_client.latest_block()
      delta = default_gtb(order['flags'])
      gtb = latest_block.block.header.height + delta

    if (gtbt := order.get('good_til_block_time')) is None and order.get('flags') == 'LONG_TERM':
      gtbt = latest_block.block.header.time.seconds + 2*delta # buffer over the usual ~1 block per second
      gtb = None

    return self.build_order(market=market, order=order, good_til_block=gtb, good_til_block_time=gtbt)

  async def place_order(self, market: PerpetualMarket, order: Order, *, unsafe: bool = False) -> OrderResponse:
    order = await self.build_order_now(market, order)
    tx: BroadcastTxResponse = await self.node_client.place_order(self.wallet, order)
    if unsafe and tx.tx_response.code != 0:
      raise ApiError(tx)
    return {
      'tx': tx,
      'order': order,
    }