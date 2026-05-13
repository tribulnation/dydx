"""Cosmos bank total supply query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.bank import v1beta1 as bank_proto
from dydx.protos.cosmos.base.query import v1beta1 as query_proto

class TotalSupply(GrpcEndpoint):
  """Bank total supply endpoint."""

  async def total_supply(
    self, *, pagination: query_proto.PageRequest | None = None,
  ) -> bank_proto.QueryTotalSupplyResponse:
    """Query total token supply."""
    request = bank_proto.QueryTotalSupplyRequest(pagination=pagination)
    return await bank_proto.QueryStub(self.channel).total_supply(request)
