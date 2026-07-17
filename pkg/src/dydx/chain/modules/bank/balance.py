"""Cosmos bank balance query."""

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.protos.cosmos.bank import v1beta1 as bank_proto

class Balance(GrpcEndpoint):
  """Bank balance endpoint."""

  @wrap_exceptions
  async def balance(self, *, address: str, denom: str) -> bank_proto.QueryBalanceResponse:
    """Query one denom balance for an account address."""
    return await bank_proto.QueryStub(self.channel).balance(
      bank_proto.QueryBalanceRequest(address=address, denom=denom)
    )
