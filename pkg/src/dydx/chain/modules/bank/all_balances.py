"""Cosmos bank all balances query."""

from typed_core import PaginatedResponse

from dydx.chain.core import GrpcEndpoint, wrap_exceptions
from dydx.chain.pagination import next_key, page_request
from dydx.protos.cosmos.bank import v1beta1 as bank_proto
from dydx.protos.cosmos.base import v1beta1 as coin_proto
from dydx.protos.cosmos.base.query import v1beta1 as query_proto

class AllBalances(GrpcEndpoint):
  """Bank all balances endpoint."""

  @wrap_exceptions
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

  def all_balances_paged(
    self, address: str, *, limit: int | None = None, resolve_denom: bool = False,
  ) -> PaginatedResponse[coin_proto.Coin, bytes]:
    """Page through all balances for an account address.

    Args:
      address: Account address to query.
      limit: Optional maximum number of balances per page.
      resolve_denom: Resolve denoms into human-readable metadata when supported.

    Returns:
      A paginated response yielding balance pages.
    """
    async def next(key: bytes) -> tuple[list[coin_proto.Coin], bytes | None]:
      """Fetch the next balance page."""
      response = await self.all_balances(
        address,
        pagination=page_request(key, limit=limit),
        resolve_denom=resolve_denom,
      )
      return response.balances, next_key(response)

    return PaginatedResponse(b'', next)
