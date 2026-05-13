"""Cosmos bank denom supply query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.bank import v1beta1 as bank_proto

class Supply(GrpcEndpoint):
  """Bank denom supply endpoint."""

  async def supply_of(self, denom: str) -> bank_proto.QuerySupplyOfResponse:
    """Query supply for one denom."""
    return await bank_proto.QueryStub(self.channel).supply_of(bank_proto.QuerySupplyOfRequest(denom=denom))
