from dataclasses import dataclass
from dydx_v4_client.indexer.rest.indexer_client import IndexerClient

@dataclass
class MarketDataMixin:
  indexer: IndexerClient
  validate: bool = True

  @classmethod
  def new(cls, url: str = 'https://indexer.dydx.trade/'):
    return cls(indexer=IndexerClient(url))