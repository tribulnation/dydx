import os
import asyncio
from dataclasses import dataclass, field

from dydx_v4_client.node.client import NodeClient, Builder, SequenceManager, QueryNodeClient
from dydx_v4_client.key_pair import KeyPair
from dydx_v4_client.wallet import Wallet
from dydx_v4_client.network import make_mainnet, make_secure, testnet_node

from dydx.indexer import INDEXER_HTTP_URL, INDEXER_WS_URL, INDEXER_TESTNET_HTTP_URL, INDEXER_TESTNET_WS_URL

OEGS_GRPC_URL = 'oegs.dydx.trade:443'
TESTNET_GRPC_URL = 'test-dydx-grpc.kingnodes.com'

def make_node_client(
  url: str, *, rest_indexer: str = INDEXER_HTTP_URL,
  websocket_indexer: str = INDEXER_WS_URL,
) -> NodeClient:
  config = make_mainnet( 
    node_url=url,
    rest_indexer=rest_indexer, 
    websocket_indexer=websocket_indexer, 
  ).node
  node = NodeClient(config.channel, Builder(config.chain_id, config.usdc_denom))
  if node.manage_sequence:
    node.sequence_manager = SequenceManager(QueryNodeClient(node.channel))
  return node

def make_testnet_node_client(
  url: str, *, rest_indexer: str = INDEXER_TESTNET_HTTP_URL,
  websocket_indexer: str = INDEXER_TESTNET_WS_URL,
) -> NodeClient:
  config = make_secure(
    testnet_node,
    node_url=url,
    rest_indexer=rest_indexer,
    websocket_indexer=websocket_indexer,
  ).node
  node = NodeClient(config.channel, Builder(config.chain_id, config.usdc_denom))
  if node.manage_sequence:
    node.sequence_manager = SequenceManager(QueryNodeClient(node.channel))
  return node

async def load_wallet(node: NodeClient, mnemonic: str):
  pair = KeyPair.from_mnemonic(mnemonic)
  address = Wallet(pair, 0, 0).address
  return await Wallet.from_mnemonic(node, mnemonic, address)

@dataclass
class PublicNodeMixin:
  node_client: NodeClient = field(kw_only=True)
  
  @classmethod
  def public(
    cls, *, url: str = OEGS_GRPC_URL,
    rest_indexer: str = INDEXER_HTTP_URL,
    websocket_indexer: str = INDEXER_WS_URL,
  ):
    return cls(
      node_client=make_node_client(url, rest_indexer=rest_indexer, websocket_indexer=websocket_indexer),
    )

  @classmethod
  def public_testnet(
    cls, *, url: str = TESTNET_GRPC_URL,
    rest_indexer: str = INDEXER_TESTNET_HTTP_URL,
    websocket_indexer: str = INDEXER_TESTNET_WS_URL,
  ):
    return cls(
      node_client=make_testnet_node_client(url, rest_indexer=rest_indexer, websocket_indexer=websocket_indexer),
    )

  async def __aenter__(self):
    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    ...

@dataclass(kw_only=True)
class PrivateNodeMixin(PublicNodeMixin):
  mnemonic: str = field(repr=False)
  lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False, repr=False)
  wallet_future: asyncio.Future[Wallet] = field(default_factory=asyncio.Future, init=False, repr=False)

  @property
  async def address(self) -> str:
    return (await self.wallet).address

  @property
  async def wallet(self) -> Wallet:
    if self.lock.locked() or self.wallet_future.done():
      return await self.wallet_future

    async with self.lock:
      wallet = await load_wallet(self.node_client, self.mnemonic)
      self.wallet_future.set_result(wallet)
      return wallet

  async def __aenter__(self):
    await self.wallet
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    self.wallet_future.cancel()
    self.wallet_future = asyncio.Future()
  
  @classmethod
  def new(
    cls, mnemonic: str | None = None, *, url: str = OEGS_GRPC_URL,
    rest_indexer: str = INDEXER_HTTP_URL,
    websocket_indexer: str = INDEXER_WS_URL,
  ):
    if mnemonic is None:
      mnemonic = os.environ['DYDX_MNEMONIC']
    node_client = make_node_client(url, rest_indexer=rest_indexer, websocket_indexer=websocket_indexer)
    return cls(node_client=node_client, mnemonic=mnemonic)

  @classmethod
  def testnet(
    cls, mnemonic: str | None = None, *, url: str = TESTNET_GRPC_URL,
    rest_indexer: str = INDEXER_TESTNET_HTTP_URL,
    websocket_indexer: str = INDEXER_TESTNET_WS_URL,
  ):
    if mnemonic is None:
      mnemonic = os.environ['DYDX_TESTNET_MNEMONIC']
    node_client = make_testnet_node_client(url, rest_indexer=rest_indexer, websocket_indexer=websocket_indexer)
    return cls(node_client=node_client, mnemonic=mnemonic)