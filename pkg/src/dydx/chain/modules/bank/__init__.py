"""Cosmos bank module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.bank.all_balances import AllBalances
from dydx.chain.modules.bank.balance import Balance
from dydx.chain.modules.bank.denom_metadata import DenomMetadata
from dydx.chain.modules.bank.denom_metadata_by_query_string import DenomMetadataByQueryString
from dydx.chain.modules.bank.denoms_metadata import DenomsMetadata
from dydx.chain.modules.bank.params import Params
from dydx.chain.modules.bank.spendable_balances import SpendableBalances
from dydx.chain.modules.bank.supply import Supply
from dydx.chain.modules.bank.total_supply import TotalSupply

class Bank(
  AllBalances,
  Balance,
  DenomMetadata,
  DenomMetadataByQueryString,
  DenomsMetadata,
  Params,
  SpendableBalances,
  Supply,
  TotalSupply,
  GrpcEndpoint,
):
  """Cosmos bank query group."""
