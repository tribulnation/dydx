from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing_extensions import Literal, NotRequired, TypedDict
from ..core import IndexerMixin, response_parser

class Order(TypedDict):
  id: str
  subaccountId: str
  clientId: str
  clobPairId: str
  side: Literal['BUY', 'SELL']
  size: Decimal
  totalFilled: Decimal
  price: Decimal
  type: Literal['LIMIT', 'MARKET', 'STOP_LIMIT', 'STOP_MARKET', 'TRAILING_STOP', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'HARD_TRADE', 'FAILED_HARD_TRADE', 'TRANSFER_PLACEHOLDER']
  status: Literal['OPEN', 'FILLED', 'CANCELED', 'BEST_EFFORT_CANCELED', 'UNTRIGGERED', 'BEST_EFFORT_OPENED', 'PENDING']
  timeInForce: Literal['GTT', 'IOC', 'FOK']
  reduceOnly: NotRequired[bool | None]
  orderFlags: str
  goodTilBlock: NotRequired[str | None]
  goodTilBlockTime: NotRequired[datetime | None]
  createdAtHeight: NotRequired[str | None]
  clientMetadata: NotRequired[str | None]
  triggerPrice: NotRequired[Decimal | None]
  postOnly: NotRequired[bool | None]
  ticker: str
  updatedAt: NotRequired[datetime | None]
  updatedAtHeight: NotRequired[str | None]
  subaccountNumber: int
  orderRouterAddress: NotRequired[str|None]
  builderFee: NotRequired[Decimal | None]
  feePpm: NotRequired[Decimal | None]

parse_response = response_parser(Order)

@dataclass
class GetOrder(IndexerMixin):
  async def get_order(
    self,
    order_id: str,
    validate: bool | None = None
  ) -> Order:
    """
    Retrieve a single order by order id.

    - `order_id`: Order id.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http#get-order)
    """
    r = await self.request('GET', f'/v4/orders/{order_id}')
    return parse_response(r, validate=self.validate(validate))

