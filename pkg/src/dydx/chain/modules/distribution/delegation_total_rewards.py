"""Cosmos distribution delegation total rewards query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.distribution import v1beta1 as distribution_proto

class DelegationTotalRewards(GrpcEndpoint):
  """Delegation total rewards endpoint."""

  async def delegation_total_rewards(self, delegator_address: str) -> distribution_proto.QueryDelegationTotalRewardsResponse:
    """Query total rewards for a delegator."""
    return await distribution_proto.QueryStub(self.channel).delegation_total_rewards(
      distribution_proto.QueryDelegationTotalRewardsRequest(delegator_address=delegator_address)
    )
