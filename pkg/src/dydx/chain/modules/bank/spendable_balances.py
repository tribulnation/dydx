"""Cosmos bank spendable balances query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.bank import v1beta1 as bank_proto
from dydx.protos.cosmos.base.query import v1beta1 as query_proto

class SpendableBalances(GrpcEndpoint):
  """Bank spendable balances endpoint."""

  async def spendable_balances(
    self, address: str, *, pagination: query_proto.PageRequest | None = None,
  ) -> bank_proto.QuerySpendableBalancesResponse:
    """Query spendable balances for an account address."""
    request = bank_proto.QuerySpendableBalancesRequest(address=address, pagination=pagination)
    return await bank_proto.QueryStub(self.channel).spendable_balances(request)
