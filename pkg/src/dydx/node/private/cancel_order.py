from dataclasses import dataclass

from dydx_v4_client import OrderFlags
from dydx_v4_client.node.builder import TxOptions
from v4_proto.dydxprotocol.clob.tx_pb2 import MsgCancelOrder
from v4_proto.dydxprotocol.clob.order_pb2 import OrderId
from v4_proto.cosmos.tx.v1beta1.service_pb2 import BroadcastTxResponse, BroadcastMode

from typed_core.exceptions import ApiError
from dydx.core import SHORT_BLOCK_WINDOW, STATEFUL_ORDER_TIME_WINDOW
from dydx.node.core import PrivateNodeMixin

@dataclass
class CancelOrder(PrivateNodeMixin):
  async def cancel_order(
    self, order_id: OrderId, *,
    good_til_block: int | None = None,
    good_til_block_time: int | None = None,
    mode: BroadcastMode = BroadcastMode.BROADCAST_MODE_SYNC,
    tx_options: TxOptions | None = None,
  ) -> BroadcastTxResponse:
    """Cancel an order.
    
    - `order_id`: order to cancel
    - `good_til_block`: block number to cancel the order at (defaults to the current one)
    - `good_til_block_time`: timestamp to cancel the order at (defaults to now)

    > [dYdX API docs](https://docs.dydx.xyz/node-client/private#cancel-order)
    """
    # SHORT-TERM orders required good_til_block
    if good_til_block is None and order_id.order_flags == OrderFlags.SHORT_TERM:
      latest_block = await self.node_client.latest_block()
      good_til_block = latest_block.block.header.height + SHORT_BLOCK_WINDOW
    # LONG-TERM orders required good_til_block_time
    elif good_til_block_time is None and order_id.order_flags == OrderFlags.LONG_TERM:
      latest_block = await self.node_client.latest_block()
      good_til_block_time = latest_block.block.header.time.seconds + STATEFUL_ORDER_TIME_WINDOW

    wallet = await self.wallet
    tx = MsgCancelOrder(order_id=order_id, good_til_block=good_til_block, good_til_block_time=good_til_block_time)
    r: BroadcastTxResponse = await self.node_client.broadcast_message(
      wallet, tx, mode=mode, tx_options=tx_options # type: ignore
    )
    if r.tx_response.code != 0:
      raise ApiError(r.tx_response.code, r.tx_response)
    return r