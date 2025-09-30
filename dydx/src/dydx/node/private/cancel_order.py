import time
from dataclasses import dataclass

from dydx_v4_client import OrderFlags
from v4_proto.dydxprotocol.clob.order_pb2 import OrderId
from v4_proto.cosmos.tx.v1beta1.service_pb2 import BroadcastTxResponse

from dydx.core import ApiError
from dydx.node.private.core import PrivateNodeMixin

@dataclass
class CancelOrder(PrivateNodeMixin):
  async def cancel_order(
    self, order_id: OrderId, *,
    good_til_block: int | None = None,
    good_til_block_time: int | None = None,
    unsafe: bool = False,
  ) -> BroadcastTxResponse:
    if order_id.order_flags & OrderFlags.LONG_TERM:
      good_til_block_time = good_til_block_time or int(time.time()) + 3600*24
    r: BroadcastTxResponse = await self.node_client.cancel_order(self.wallet, order_id, good_til_block=good_til_block, good_til_block_time=good_til_block_time)
    if unsafe and r.tx_response.code != 0:
      raise ApiError(r)
    return r