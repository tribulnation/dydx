"""Cosmos Tendermint latest validator set query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.cosmos.base.tendermint import v1beta1 as tendermint_proto

class ValidatorSets(GrpcEndpoint):
  """Tendermint latest validator set endpoint."""

  async def get_latest_validator_set(
    self, *, pagination: query_proto.PageRequest | None = None,
  ) -> tendermint_proto.GetLatestValidatorSetResponse:
    """Query the latest validator set."""
    request = tendermint_proto.GetLatestValidatorSetRequest(pagination=pagination)
    return await tendermint_proto.ServiceStub(self.channel).get_latest_validator_set(request)
