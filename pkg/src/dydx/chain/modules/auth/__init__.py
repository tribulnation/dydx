"""Cosmos auth module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.auth.account import Account
from dydx.chain.modules.auth.account_info import AccountInfo
from dydx.chain.modules.auth.accounts import Accounts

class Auth(Account, AccountInfo, Accounts, GrpcEndpoint):
  """Cosmos auth query group."""
