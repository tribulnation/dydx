"""dYdX subaccount query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.dydxprotocol import subaccounts as subaccounts_proto

class Subaccount(GrpcEndpoint):
  """Subaccount endpoint."""

  @wrap_exceptions
  async def subaccount(self, owner: str, number: int = 0) -> subaccounts_proto.QuerySubaccountResponse:
    """Query a subaccount by owner and number."""
    return await subaccounts_proto.QueryStub(self.channel).subaccount(subaccounts_proto.QueryGetSubaccountRequest(owner=owner, number=number))
