from dataclasses import dataclass, field
from dydx_v4_client.node.client import NodeClient
from dydx_v4_client.key_pair import KeyPair
from dydx_v4_client.wallet import Wallet
from dydx_v4_client.network import make_mainnet

POLKACHU_GRPC_URL = 'https://dydx-dao-grpc-1.polkachu.com:443'

@dataclass
class PrivateNodeMixin:
  address: str = field(kw_only=True)
  node_client: NodeClient = field(kw_only=True)
  wallet: Wallet = field(kw_only=True)
  
  @classmethod
  async def connect(cls, mnemonic: str, *, url: str = POLKACHU_GRPC_URL):
    pair = KeyPair.from_mnemonic(mnemonic)
    address = Wallet(pair, 0, 0).address
    config = make_mainnet( 
      node_url=url,
      rest_indexer='', 
      websocket_indexer='', 
    ).node
    node: NodeClient = await NodeClient.connect(config)
    wallet = await Wallet.from_mnemonic(node, mnemonic, address)
    return cls(node_client=node, wallet=wallet, address=address)