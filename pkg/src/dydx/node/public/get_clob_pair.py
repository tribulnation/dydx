from dataclasses import dataclass

from grpc._channel import _InactiveRpcError

from v4_proto.dydxprotocol.clob.clob_pair_pb2 import ClobPair
from typed_core.exceptions import ApiError
from dydx.node.core import PublicNodeMixin

@dataclass
class GetClobPair(PublicNodeMixin):
  async def get_clob_pair(self, id: int) -> ClobPair:
    """
    Fetches the order book pair identified by a given ID, allowing users to retrieve detailed information about a specific trading pair within a Central Limit Order Book (CLOB) system.

    - `id`: The id of the CLOB pair.

    > [dYdX API docs](https://docs.dydx.xyz/node-client/public#get-clob-pair)
    """
    try:
      return await self.node_client.get_clob_pair(id)
    except _InactiveRpcError as e:
      raise ApiError(e._state.code, e._state.details)