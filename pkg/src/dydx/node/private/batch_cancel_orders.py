from typing_extensions import Sequence
from dataclasses import dataclass
from collections import defaultdict

from dydx_v4_client import OrderFlags
from v4_proto.dydxprotocol.clob.tx_pb2 import OrderBatch
from v4_proto.dydxprotocol.clob.order_pb2 import OrderId
from v4_proto.cosmos.tx.v1beta1.service_pb2 import BroadcastTxResponse

from dydx.core import ApiError, UserError, SHORT_BLOCK_WINDOW
from dydx.node.core import PrivateNodeMixin

@dataclass
class BatchCancelOrders(PrivateNodeMixin):
  async def batch_cancel_orders(
    self, order_ids: Sequence[OrderId], *,
    good_til_block: int | None = None,
  ) -> BroadcastTxResponse:
    """Cancel an order.
    
    - `order_ids`: orders to cancel
    - `good_til_block`: block number to cancel the orders at (defaults to the current one)

    > [dYdX API docs](https://docs.dydx.xyz/node-client/private#cancel-order)
    """
    subaccount_id = order_ids[0].subaccount_id
    orders_by_pair = defaultdict[int, list[int]](list)
    for order_id in order_ids:
      if order_id.order_flags != OrderFlags.SHORT_TERM:
        raise UserError('Only short-term orders can be cancelled in a batch')
      orders_by_pair[order_id.clob_pair_id].append(order_id.client_id)

    batches = [
      OrderBatch(clob_pair_id=pair, client_ids=orders)
      for pair, orders in orders_by_pair.items()
    ]

    if good_til_block is None:
      latest_block = await self.node_client.latest_block()
      good_til_block = latest_block.block.header.height + SHORT_BLOCK_WINDOW

    r: BroadcastTxResponse = await self.node_client.batch_cancel_orders(
      wallet=self.wallet, subaccount_id=subaccount_id,
      short_term_cancels=batches,
      good_til_block=good_til_block,
    )
    if r.tx_response.code != 0:
      raise ApiError(r.tx_response.code, r.tx_response)
    return r