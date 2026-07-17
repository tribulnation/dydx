"""Cosmos auth account query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.gov import v1 as gov_proto
from dydx.protos.cosmos.base.query import v1beta1 as query_proto

class Proposals(GrpcEndpoint):
  @wrap_exceptions
  async def proposals(
    self, *, status: gov_proto.ProposalStatus | None = None,
    voter: str | None = None, depositor: str | None = None,
    pagination: query_proto.PageRequest | None = None
  ) -> gov_proto.QueryProposalsResponse:
    """Query governance proposals.
    
    Args:
      status: Optional proposal status to filter by.
      voter: Optional voter address to filter by.
      depositor: Optional depositor address to filter by.
      pagination: Optional pagination to use for the query.

    Returns:
      A list of governance proposals.
    """
    return await gov_proto.QueryStub(self.channel).proposals(gov_proto.QueryProposalsRequest(
      proposal_status=status or gov_proto.ProposalStatus.UNSPECIFIED,
      voter=voter or '',
      depositor=depositor or '',
      pagination=pagination,
    ))

  
  def proposals_paged(
    self, *, limit: int | None = None, status: gov_proto.ProposalStatus | None = None,
    voter: str | None = None, depositor: str | None = None,
  ) -> PaginatedResponse[gov_proto.Proposal, bytes]:
    """Page through governance proposals.
    
    Args:
      limit: Optional maximum number of proposals per page.
      status: Optional proposal status to filter by.
      voter: Optional voter address to filter by.
      depositor: Optional depositor address to filter by.

    Returns:
      A paginated response yielding proposal pages.
    """
    async def next(key: bytes) -> tuple[list[gov_proto.Proposal], bytes | None]:
      """Fetch the next proposal page."""
      response = await self.proposals(
        status=status,
        voter=voter,
        depositor=depositor,
        pagination=page_request(key, limit=limit),
      )
      return response.proposals, next_key(response)

    return PaginatedResponse(b'', next)
  
