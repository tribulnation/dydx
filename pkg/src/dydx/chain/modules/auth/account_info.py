"""Cosmos auth account info query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.cosmos.auth import v1beta1 as auth_proto

class AccountInfo(GrpcEndpoint):
  """Auth account info endpoint."""

  @wrap_exceptions
  async def account_info(self, address: str) -> auth_proto.QueryAccountInfoResponse:
    """Query account sequence and number information."""
    return await auth_proto.QueryStub(self.channel).account_info(auth_proto.QueryAccountInfoRequest(address=address))
