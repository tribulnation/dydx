from dataclasses import dataclass

from dydx.indexer.types import OrderState
from .core import IndexerMixin, response_parser

parse_response = response_parser(OrderState)

@dataclass
class GetOrder(IndexerMixin):
  async def get_order(self, id: str, *, validate: bool | None = None) -> OrderState:
    """Retrieves detailed information about a specific order based on its unique identifier (the order ID).

    - `id`: The ID of the order to retrieve.
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-order)
    """
    r = await self.request('GET', f'/v4/orders/{id}')
    return parse_response(r, validate=self.validate(validate))