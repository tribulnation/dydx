from dataclasses import dataclass
from dydx.indexer import IndexerData, INDEXER_HTTP_URL, IndexerStreams, INDEXER_WS_URL

@dataclass(kw_only=True)
class MarketDataMixin:
  indexer_data: IndexerData

  @classmethod
  def new(cls, url: str = INDEXER_HTTP_URL, *, validate: bool = True):
    return cls(indexer_data=IndexerData(url=url, default_validate=validate))

@dataclass(kw_only=True)
class UserDataMixin:
  address: str
  subaccount: int
  indexer_data: IndexerData

  @classmethod
  def new(cls, address: str, *, subaccount: int, url: str = INDEXER_HTTP_URL, validate: bool = True):
    return cls(address=address, subaccount=subaccount, indexer_data=IndexerData(url=url, default_validate=validate))


@dataclass(kw_only=True)
class UserStreamsMixin:
  address: str
  subaccount: int
  indexer_streams: IndexerStreams

  @classmethod
  def new(cls, address: str, *, subaccount: int, url: str = INDEXER_WS_URL, validate: bool = True):
    return cls(address=address, subaccount=subaccount, indexer_streams=IndexerStreams.new(url=url, validate=validate))
