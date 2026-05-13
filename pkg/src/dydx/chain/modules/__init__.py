"""dYdX Chain module groups."""

from typing_extensions import Self, TypedDict, Unpack

from dydx.chain.core import GrpcClient, GrpcRouter
from dydx.chain.modules.affiliates import Affiliates
from dydx.chain.modules.assets import Assets
from dydx.chain.modules.auth import Auth
from dydx.chain.modules.bank import Bank
from dydx.chain.modules.clob import Clob
from dydx.chain.modules.distribution import Distribution
from dydx.chain.modules.feetiers import Feetiers
from dydx.chain.modules.perpetuals import Perpetuals
from dydx.chain.modules.prices import Prices
from dydx.chain.modules.revshare import Revshare
from dydx.chain.modules.rewards import Rewards
from dydx.chain.modules.staking import Staking
from dydx.chain.modules.subaccounts import Subaccounts
from dydx.chain.modules.tendermint import Tendermint
from dydx.chain.modules.tx import Tx

DYDX_GRPC_OEGS_HOST = 'oegs.dydx.trade'
DYDX_GRPC_POLKACHU_1_HOST = 'dydx-dao-grpc-1.polkachu.com'
DYDX_GRPC_POLKACHU_2_HOST = 'dydx-dao-grpc-2.polkachu.com'
DYDX_GRPC_POLKACHU_3_HOST = 'dydx-dao-grpc-3.polkachu.com'
DYDX_GRPC_KINGNODES_HOST = 'dydx-ops-grpc.kingnodes.com'
DYDX_GRPC_ENIGMA_HOST = 'dydx-dao-grpc.enigma-validator.com'
DYDX_GRPC_POLKACHU_ARCHIVE_1_HOST = 'dydx-dao-archive-grpc-1.polkachu.com'
DYDX_GRPC_KINGNODES_ARCHIVE_HOST = 'dydx-ops-archive-grpc.kingnodes.com'
DYDX_GRPC_ENIGMA_ARCHIVE_HOST = 'dydx-dao-grpc-archive.enigma-validator.com'
DYDX_GRPC_HOSTS = (
  DYDX_GRPC_OEGS_HOST,
  DYDX_GRPC_POLKACHU_1_HOST,
  DYDX_GRPC_POLKACHU_2_HOST,
  DYDX_GRPC_POLKACHU_3_HOST,
  DYDX_GRPC_KINGNODES_HOST,
  DYDX_GRPC_ENIGMA_HOST,
)
DYDX_GRPC_ARCHIVE_HOSTS = (
  DYDX_GRPC_POLKACHU_ARCHIVE_1_HOST,
  DYDX_GRPC_KINGNODES_ARCHIVE_HOST,
  DYDX_GRPC_ENIGMA_ARCHIVE_HOST,
)

DYDX_TESTNET_GRPC_OEGS_HOST = 'oegs-testnet.dydx.exchange'
DYDX_TESTNET_GRPC_KINGNODES_HOST = 'test-dydx-grpc.kingnodes.com'
DYDX_TESTNET_GRPC_POLKACHU_HOST = 'dydx-testnet-grpc.polkachu.com'
DYDX_TESTNET_GRPC_HOSTS = (
  DYDX_TESTNET_GRPC_OEGS_HOST,
  DYDX_TESTNET_GRPC_KINGNODES_HOST,
  DYDX_TESTNET_GRPC_POLKACHU_HOST,
)

class ModulesOptions(TypedDict, total=False):
  """Options shared by gRPC module constructors."""

  client: GrpcClient
  """Existing gRPC transport shared by module adapters."""

class GrpcOptions(TypedDict, total=False):
  """Options for constructing a gRPC transport."""

  port: int
  """gRPC endpoint port."""
  ssl: bool
  """Use TLS for the gRPC channel."""

class Modules(GrpcRouter):
  """Composed dYdX Chain module groups."""

  auth: Auth
  bank: Bank
  tx: Tx
  tendermint: Tendermint
  staking: Staking
  distribution: Distribution
  subaccounts: Subaccounts
  clob: Clob
  prices: Prices
  perpetuals: Perpetuals
  assets: Assets
  feetiers: Feetiers
  rewards: Rewards
  affiliates: Affiliates
  revshare: Revshare

  @classmethod
  def new(cls, host: str, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for a custom gRPC endpoint."""
    return cls(client=GrpcClient(host=host, **kwargs))

  @classmethod
  def from_client(cls, client: GrpcClient) -> Self:
    """Create module groups from an existing gRPC transport."""
    return cls(client=client)

  @classmethod
  def oegs(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the OEGS mainnet gRPC endpoint."""
    return cls.new(DYDX_GRPC_OEGS_HOST, **kwargs)

  @classmethod
  def polkachu(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the first Polkachu mainnet gRPC endpoint."""
    return cls.new(DYDX_GRPC_POLKACHU_1_HOST, **kwargs)

  @classmethod
  def polkachu_2(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the second Polkachu mainnet gRPC endpoint."""
    return cls.new(DYDX_GRPC_POLKACHU_2_HOST, **kwargs)

  @classmethod
  def polkachu_3(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the third Polkachu mainnet gRPC endpoint."""
    return cls.new(DYDX_GRPC_POLKACHU_3_HOST, **kwargs)

  @classmethod
  def kingnodes(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the KingNodes mainnet gRPC endpoint."""
    return cls.new(DYDX_GRPC_KINGNODES_HOST, **kwargs)

  @classmethod
  def enigma(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the Enigma mainnet gRPC endpoint."""
    return cls.new(DYDX_GRPC_ENIGMA_HOST, **kwargs)

  @classmethod
  def polkachu_archive(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the Polkachu archive mainnet gRPC endpoint."""
    return cls.new(DYDX_GRPC_POLKACHU_ARCHIVE_1_HOST, **kwargs)

  @classmethod
  def kingnodes_archive(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the KingNodes archive mainnet gRPC endpoint."""
    return cls.new(DYDX_GRPC_KINGNODES_ARCHIVE_HOST, **kwargs)

  @classmethod
  def enigma_archive(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the Enigma archive mainnet gRPC endpoint."""
    return cls.new(DYDX_GRPC_ENIGMA_ARCHIVE_HOST, **kwargs)

  @classmethod
  def testnet_oegs(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the OEGS testnet gRPC endpoint."""
    return cls.new(DYDX_TESTNET_GRPC_OEGS_HOST, **kwargs)

  @classmethod
  def testnet_kingnodes(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the KingNodes testnet gRPC endpoint."""
    return cls.new(DYDX_TESTNET_GRPC_KINGNODES_HOST, **kwargs)

  @classmethod
  def testnet_polkachu(cls, **kwargs: Unpack[GrpcOptions]) -> Self:
    """Create module groups for the Polkachu plaintext testnet gRPC endpoint."""
    port = kwargs.get('port', 23890)
    ssl = kwargs.get('ssl', False)
    return cls.new(DYDX_TESTNET_GRPC_POLKACHU_HOST, port=port, ssl=ssl)
