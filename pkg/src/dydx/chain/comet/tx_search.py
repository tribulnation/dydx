"""Comet transaction search endpoint."""

from pydantic import TypeAdapter
from typing_extensions import Literal

from dydx.chain.comet.core import CometEndpoint
from dydx.chain.comet.types import TxSearchResponse


tx_search_adapter = TypeAdapter(TxSearchResponse)


class TxSearch(CometEndpoint):
  """Comet transaction search endpoint group."""

  async def tx_search(
    self,
    query: str,
    *,
    prove: bool | None = None,
    page: int | None = None,
    per_page: int | None = None,
    order_by: Literal['asc', 'desc'] | None = None,
    validate: bool | None = None,
  ) -> TxSearchResponse:
    """Search indexed Comet transactions by event query.

    Args:
      query: Comet event query expression.
      prove: Include proofs for returned transactions.
      page: Page number for paginated results.
      per_page: Maximum transactions to return on the page.
      order_by: Sort order for matching transactions.
      validate: Validation override for this request.

    Returns:
      Transaction search result.

    References:
      - [CometBFT RPC docs](https://docs.cosmos.network/cometbft/latest/api-reference/rpc/info/tx_search)
    """
    params: dict[str, str | bool | int] = {'query': f'"{query}"'}
    if prove is not None:
      params['prove'] = prove
    if page is not None:
      params['page'] = page
    if per_page is not None:
      params['per_page'] = per_page
    if order_by is not None:
      params['order_by'] = order_by
    return await self.result('/tx_search', params=params, result_adapter=tx_search_adapter, validate=validate)

