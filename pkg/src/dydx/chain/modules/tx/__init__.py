"""Cosmos tx service module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.tx.broadcast import Broadcast
from dydx.chain.modules.tx.get_tx import GetTx
from dydx.chain.modules.tx.get_txs_event import GetTxsEvent
from dydx.chain.modules.tx.simulate import Simulate

class Tx(Broadcast, GetTx, GetTxsEvent, Simulate, GrpcEndpoint):
  """Cosmos transaction service group."""
