from typing_extensions import Literal, overload
from dataclasses import dataclass
from datetime import datetime

from dydx.core.types import OrderState
from .core import IndexerMixin, response_parser, Response

parse_response = response_parser(OrderState)

@dataclass
class GetOrder(IndexerMixin):
  @overload
  async def get_order(self, orderId: str, *, validate: bool | None = None, unsafe: Literal[True] = True) -> OrderState:
    ...
  @overload
  async def get_order(self, orderId: str, *, validate: bool | None = None) -> Response[OrderState]:
    ...
  async def get_order(
    self, orderId: str, *, validate: bool | None = None, unsafe: bool = False,
  ) -> Response[OrderState] | OrderState:
    """Retrieves detailed information about a specific order based on its unique identifier (the order ID).

    - `orderId`: The ID of the order to retrieve.
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-order)
    """
    r = await self.request('GET', f'/v4/orders/{orderId}')
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))