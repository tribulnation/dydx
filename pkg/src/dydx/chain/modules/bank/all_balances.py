"""Cosmos bank all balances query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.bank import v1beta1 as bank_proto
from dydx.protos.cosmos.base.query import v1beta1 as query_proto

class AllBalances(GrpcEndpoint):
  """Bank all balances endpoint."""

  async def all_balances(
    self, address: str, *, pagination: query_proto.PageRequest | None = None, resolve_denom: bool = False,
  ) -> bank_proto.QueryAllBalancesResponse:
    """Query all balances for an account address."""
    request = bank_proto.QueryAllBalancesRequest(
      address=address,
      pagination=pagination,
      resolve_denom=resolve_denom,
    )
    return await bank_proto.QueryStub(self.channel).all_balances(request)
