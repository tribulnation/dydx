"""Cosmos Tendermint service module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.tendermint.get_block_by_height import GetBlockByHeight
from dydx.chain.modules.tendermint.get_latest_block import GetLatestBlock
from dydx.chain.modules.tendermint.get_node_info import GetNodeInfo
from dydx.chain.modules.tendermint.get_validator_set_by_height import GetValidatorSetByHeight
from dydx.chain.modules.tendermint.validator_sets import ValidatorSets

class Tendermint(
  GetBlockByHeight,
  GetLatestBlock,
  GetNodeInfo,
  GetValidatorSetByHeight,
  ValidatorSets,
  GrpcEndpoint,
):
  """Cosmos Tendermint query group."""
