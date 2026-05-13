"""dYdX CLOB module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.clob.clob_pair import ClobPair
from dydx.chain.modules.clob.clob_pairs import ClobPairs
from dydx.chain.modules.clob.leverage import Leverage

class Clob(ClobPair, ClobPairs, Leverage, GrpcEndpoint):
  """dYdX CLOB query group."""
