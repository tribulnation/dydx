from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing_extensions import Literal, NotRequired, TypedDict
from ..core import IndexerMixin, response_parser

class PerpetualPosition(TypedDict):
  market: str
  status: Literal['OPEN', 'CLOSED', 'LIQUIDATED']
  side: Literal['LONG', 'SHORT']
  size: Decimal
  maxSize: Decimal
  entryPrice: Decimal
  exitPrice: NotRequired[Decimal | None]
  realizedPnl: NotRequired[Decimal | None]
  unrealizedPnl: NotRequired[Decimal | None]
  createdAt: datetime
  createdAtHeight: str
  closedAt: NotRequired[datetime | None]
  sumOpen: Decimal
  sumClose: Decimal
  netFunding: Decimal
  subaccountNumber: int

parse_response = response_parser(list[PerpetualPosition])

@dataclass
class ListParentPositions(IndexerMixin):
  async def list_parent_positions(
    self,
    address: str,
    *,
    parent_subaccount: int,
    limit: int | None = None,
    validate: bool | None = None
  ) -> list[PerpetualPosition]:
    """
    List parent positions

    - `address`: Wallet address that owns the account.
    - `parent_subaccount`: Parent subaccount number.
    - `limit`: Maximum number of results to return.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/accounts#list-parent-positions)
    """
    params: dict[str, object] = {
      'address': address,
      'parentSubaccountNumber': parent_subaccount,
    }
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', '/v4/perpetualPositions/parentSubaccountNumber', params=params)
    return parse_response(r, validate=self.validate(validate))
