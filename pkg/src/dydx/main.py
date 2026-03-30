from dataclasses import dataclass
import asyncio
from .indexer import Indexer, INDEXER_HTTP_URL, INDEXER_WS_URL
from .node import Node, OEGS_GRPC_URL

@dataclass
class DYDX:
  indexer: Indexer
  node: Node

  @classmethod
  def new(
    cls, mnemonic: str | None = None, *, node_url: str = OEGS_GRPC_URL,
    rest_indexer: str = INDEXER_HTTP_URL,
    websocket_indexer: str = INDEXER_WS_URL,
    validate: bool = True,
  ):
    indexer = Indexer.new(http_url=rest_indexer, ws_url=websocket_indexer, validate=validate)
    node = Node.new(mnemonic=mnemonic, url=node_url, rest_indexer=rest_indexer, websocket_indexer=websocket_indexer)
    return cls(indexer=indexer, node=node)

  async def __aenter__(self):
    await asyncio.gather(
      self.indexer.__aenter__(),
      self.node.__aenter__(),
    )
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await asyncio.gather(
      self.indexer.__aexit__(exc_type, exc_value, traceback),
      self.node.__aexit__(exc_type, exc_value, traceback),
    )