"""Cosmos auth account query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.auth import v1beta1 as auth_proto

class Account(GrpcEndpoint):
  """Auth account endpoint."""

  async def account(self, address: str) -> auth_proto.QueryAccountResponse:
    """Query an account by address."""
    return await auth_proto.QueryStub(self.channel).account(auth_proto.QueryAccountRequest(address=address))
