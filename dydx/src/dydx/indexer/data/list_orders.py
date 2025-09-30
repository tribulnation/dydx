from typing_extensions import Literal, overload
from dataclasses import dataclass
from datetime import datetime

from dydx.core.types import OrderSide, OrderStatus, OrderType, OrderState
from .core import IndexerMixin, response_parser, Response

parse_response = response_parser(list[OrderState])

@dataclass
class ListOrders(IndexerMixin):
  @overload
  async def list_orders(
    self, address: str, *,
    subaccount: int = 0,
    limit: int | None = None,
    ticker: str | None = None,
    side: OrderSide | None = None,
    status: OrderStatus | None = None,
    type: OrderType | None = None,
    good_til_block_end: int | None = None,
    good_til_block_time_end: datetime | None = None,
    latest_only: bool | None = None,
    validate: bool | None = None,
    unsafe: Literal[True],
  ) -> list[OrderState]:
    ...
  @overload
  async def list_orders(
    self, address: str, *,
    subaccount: int = 0,
    limit: int | None = None,
    ticker: str | None = None,
    side: OrderSide | None = None,
    status: OrderStatus | None = None,
    type: OrderType | None = None,
    good_til_block_end: int | None = None,
    good_til_block_time_end: datetime | None = None,
    latest_only: bool | None = None,
    validate: bool | None = None,
  ) -> Response[list[OrderState]]:
    ...
  async def list_orders(
    self, address: str, *,
    subaccount: int = 0,
    limit: int | None = None,
    ticker: str | None = None,
    side: OrderSide | None = None,
    status: OrderStatus | None = None,
    type: OrderType | None = None,
    good_til_block_end: int | None = None,
    good_til_block_time_end: datetime | None = None,
    latest_only: bool | None = None,
    validate: bool | None = None,
    unsafe: bool = False,
  ) -> Response[list[OrderState]] | list[OrderState]:
    """Retrieves orders for a specific subaccount, with various filtering options to narrow down the results based on order characteristics.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `limit`: Maximum number of asset positions to return in the response.
    - `ticker`: The ticker filter.
    - `side`: The order side filter (LONG or SHORT).
    - `status`: The order status filter (Open, Filled, Canceled, etc).
    - `type`: The order type filter (LIMIT, MARKET, STOP_LIMIT, etc).
    - `good_til_block_end`: The block number filter for orders good until before or at.
    - `good_til_block_time_end`: The timestamp filter for orders good until before or at (UTC).
    - `latest_only`: Whether to return only the latest orders.
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#list-orders)
    """
    params = {'address': address, 'subaccountNumber': subaccount}
    if limit is not None:
      params['limit'] = limit
    if ticker is not None:
      params['ticker'] = ticker
    if side is not None:
      params['side'] = side
    if status is not None:
      params['status'] = status
    if type is not None:
      params['type'] = type
    if good_til_block_end is not None:
      params['goodTilBlockBeforeOrAt'] = good_til_block_end
    if good_til_block_time_end is not None:
      params['goodTilBlockTimeBeforeOrAt'] = good_til_block_time_end
    if latest_only is not None:
      params['returnLatestOrders'] = latest_only
    r = await self.request('GET', '/v4/orders', params=params)
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))