from dataclasses import dataclass
from .data import IndexerData, INDEXER_HTTP_URL
from .streams import IndexerStreams, INDEXER_WS_URL

@dataclass
class Indexer:
  data: IndexerData
  streams: IndexerStreams

  @classmethod
  def new(cls, *, http_url: str = INDEXER_HTTP_URL, ws_url: str = INDEXER_WS_URL, validate: bool = True):
    return cls(
      data=IndexerData(url=http_url, default_validate=validate),
      streams=IndexerStreams.new(url=ws_url, validate=validate),
    )