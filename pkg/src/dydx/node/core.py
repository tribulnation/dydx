import os
from dataclasses import dataclass, field
from dydx_v4_client.node.client import NodeClient
from dydx_v4_client.key_pair import KeyPair
from dydx_v4_client.wallet import Wallet
from dydx_v4_client.network import make_mainnet

from dydx.indexer import INDEXER_HTTP_URL, INDEXER_WS_URL

OEGS_GRPC_URL = 'oegs.dydx.trade:443'

@dataclass
class PublicNodeMixin:
  node_client: NodeClient = field(kw_only=True)
  
  @classmethod
  async def connect(
    cls, *, url: str = OEGS_GRPC_URL,
    rest_indexer: str = INDEXER_HTTP_URL,
    websocket_indexer: str = INDEXER_WS_URL,
  ):
    config = make_mainnet( 
      node_url=url,
      rest_indexer=rest_indexer, 
      websocket_indexer=websocket_indexer, 
    ).node
    node: NodeClient = await NodeClient.connect(config)
    return cls(node_client=node)

@dataclass
class PrivateNodeMixin:
  address: str = field(kw_only=True)
  node_client: NodeClient = field(kw_only=True)
  wallet: Wallet = field(kw_only=True)
  
  @classmethod
  async def connect(
    cls, mnemonic: str | None = None, *, url: str = OEGS_GRPC_URL,
    rest_indexer: str = INDEXER_HTTP_URL,
    websocket_indexer: str = INDEXER_WS_URL,
  ):
    if mnemonic is None:
      mnemonic = os.environ['DYDX_MNEMONIC']
    pair = KeyPair.from_mnemonic(mnemonic)
    address = Wallet(pair, 0, 0).address
    config = make_mainnet( 
      node_url=url,
      rest_indexer=rest_indexer, 
      websocket_indexer=websocket_indexer, 
    ).node
    node: NodeClient = await NodeClient.connect(config)
    wallet = await Wallet.from_mnemonic(node, mnemonic, address)
    return cls(node_client=node, wallet=wallet, address=address)