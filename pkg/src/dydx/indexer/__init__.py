from dataclasses import dataclass as _dataclass, field as _field
from .data import IndexerData, INDEXER_HTTP_URL
from .streams import IndexerStreams, INDEXER_WS_URL

@_dataclass
class Indexer:
  data: IndexerData = _field(default_factory=IndexerData)
  streams: IndexerStreams = _field(default_factory=IndexerStreams)

  @classmethod
  def new(cls, *, http_url: str = INDEXER_HTTP_URL, ws_url: str = INDEXER_WS_URL, validate: bool = True):
    return cls(
      data=IndexerData(url=http_url, default_validate=validate),
      streams=IndexerStreams.new(url=ws_url, validate=validate),
    )

  async def __aenter__(self):
    await self.data.__aenter__()
    await self.streams.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.data.__aexit__(exc_type, exc_value, traceback)
    await self.streams.__aexit__(exc_type, exc_value, traceback)