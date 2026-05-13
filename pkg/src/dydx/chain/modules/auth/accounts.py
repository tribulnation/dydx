"""Cosmos auth accounts query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.auth import v1beta1 as auth_proto
from dydx.protos.cosmos.base.query import v1beta1 as query_proto

class Accounts(GrpcEndpoint):
  """Auth accounts endpoint."""

  async def accounts(self, *, pagination: query_proto.PageRequest | None = None) -> auth_proto.QueryAccountsResponse:
    """Query chain accounts."""
    request = auth_proto.QueryAccountsRequest(pagination=pagination)
    return await auth_proto.QueryStub(self.channel).accounts(request)
