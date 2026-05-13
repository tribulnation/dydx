"""Cosmos bank params query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.bank import v1beta1 as bank_proto

class Params(GrpcEndpoint):
  """Bank params endpoint."""

  async def params(self) -> bank_proto.QueryParamsResponse:
    """Query bank module parameters."""
    return await bank_proto.QueryStub(self.channel).params(bank_proto.QueryParamsRequest())
