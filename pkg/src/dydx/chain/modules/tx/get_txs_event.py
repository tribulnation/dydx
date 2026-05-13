"""Cosmos tx event search query."""

from dydx.chain.core import GrpcEndpoint
from dydx.protos.cosmos.base.query import v1beta1 as query_proto
from dydx.protos.cosmos.tx import v1beta1 as tx_proto
from dydx.protos.cosmos.tx.v1beta1 import OrderBy

class GetTxsEvent(GrpcEndpoint):
  """Transaction event search endpoint."""

  async def get_txs_event(
    self,
    query: str | None = None, *,
    events: list[str] | None = None,
    pagination: query_proto.PageRequest | None = None,
    order_by: OrderBy | None = None,
    page: int | None = None,
    limit: int | None = None,
  ) -> tx_proto.GetTxsEventResponse:
    """Query transactions by event expression."""
    request = tx_proto.GetTxsEventRequest()
    if pagination is not None:
      request.pagination = pagination
    if order_by is not None:
      request.order_by = order_by
    if page is not None:
      request.page = page
    if limit is not None:
      request.limit = limit
    if query is not None:
      request.query = query
    if events:
      request.events.extend(events)
    return await tx_proto.ServiceStub(self.channel).get_txs_event(request)
