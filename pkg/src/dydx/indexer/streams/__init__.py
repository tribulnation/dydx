from dataclasses import dataclass

from .core import INDEXER_WS_URL, INDEXER_TESTNET_WS_URL
from .api.block_height import BlockHeight
from .candles import Candles
from .api.markets import Markets
from .api.orders import Orders
from .parent_subaccounts import ParentSubaccounts
from .subaccounts import Subaccounts
from .api.trades import Trades

@dataclass
class IndexerStreams(
  BlockHeight,
  Candles,
  Markets,
  Orders,
  ParentSubaccounts,
  Subaccounts,
  Trades,
):
  ...
