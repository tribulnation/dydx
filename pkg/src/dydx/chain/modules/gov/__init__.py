"""Cosmos gov module."""

from dydx.chain.core import GrpcEndpoint
from dydx.chain.modules.gov.proposals import Proposals

class Gov(Proposals, GrpcEndpoint):
  """Cosmos governance query group."""
