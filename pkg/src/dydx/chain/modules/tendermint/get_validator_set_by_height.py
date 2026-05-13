"""Cosmos Tendermint validator set by height query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.cosmos.base.tendermint import v1beta1 as tendermint_proto

class GetValidatorSetByHeight(GrpcEndpoint):
  """Tendermint validator set by height endpoint."""

  async def get_validator_set_by_height(
    self, height: int, *, pagination: query_proto.PageRequest | None = None,
  ) -> tendermint_proto.GetValidatorSetByHeightResponse:
    """Query a validator set by height."""
    request = tendermint_proto.GetValidatorSetByHeightRequest(height=height, pagination=pagination)
    return await tendermint_proto.ServiceStub(self.channel).get_validator_set_by_height(request)
