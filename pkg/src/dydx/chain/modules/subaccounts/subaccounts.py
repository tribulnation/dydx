"""dYdX subaccounts query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.dydxprotocol import subaccounts as subaccounts_proto

class SubaccountsAll(GrpcEndpoint):
  """Subaccounts list endpoint."""

  async def subaccounts(self, *, pagination: query_proto.PageRequest | None = None) -> subaccounts_proto.QuerySubaccountAllResponse:
    """Query all subaccounts."""
    request = subaccounts_proto.QueryAllSubaccountRequest(pagination=pagination)
    return await subaccounts_proto.QueryStub(self.channel).subaccount_all(request)
