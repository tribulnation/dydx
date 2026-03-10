from dataclasses import dataclass

from .core import INDEXER_WS_URL
from .subaccounts import Subaccounts

@dataclass
class IndexerStreams(Subaccounts):
  ...