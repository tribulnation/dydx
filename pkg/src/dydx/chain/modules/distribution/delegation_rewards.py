"""Cosmos distribution delegation rewards query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.distribution import v1beta1 as distribution_proto

class DelegationRewards(GrpcEndpoint):
  """Delegation rewards endpoint."""

  async def delegation_rewards(
    self, *, delegator_address: str, validator_address: str,
  ) -> distribution_proto.QueryDelegationRewardsResponse:
    """Query rewards for a delegator and validator."""
    return await distribution_proto.QueryStub(self.channel).delegation_rewards(
      distribution_proto.QueryDelegationRewardsRequest(
        delegator_address=delegator_address,
        validator_address=validator_address,
      )
    )
