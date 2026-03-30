from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing_extensions import Literal, NotRequired, TypedDict
from ..core import IndexerMixin, response_parser

class AssetPosition(TypedDict):
  size: Decimal
  symbol: str
  side: Literal['LONG', 'SHORT']
  assetId: str
  subaccountNumber: int

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

AssetPositionsMap = dict[str, AssetPosition]

PerpetualPositionsMap = dict[str, PerpetualPosition]

class Subaccount(TypedDict):
  address: str
  subaccountNumber: int
  equity: Decimal
  freeCollateral: Decimal
  openPerpetualPositions: PerpetualPositionsMap
  assetPositions: AssetPositionsMap
  marginEnabled: bool
  updatedAtHeight: str
  latestProcessedBlockHeight: str

class ParentSubaccount(TypedDict):
  address: str
  parentSubaccountNumber: int
  equity: Decimal
  freeCollateral: Decimal
  childSubaccounts: list[Subaccount]

parse_response = response_parser(ParentSubaccount)

@dataclass
class GetParentSubaccount(IndexerMixin):
  async def get_parent_subaccount(
    self,
    address: str,
    parent_subaccount: int,
    validate: bool | None = None
  ) -> ParentSubaccount:
    """
    Get parent subaccount

    - `address`: Wallet address that owns the parent subaccount.
    - `parent_subaccount`: Parent subaccount number.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/accounts#get-parent-subaccount)
    """
    r = await self.request('GET', f'/v4/addresses/{address}/parentSubaccountNumber/{parent_subaccount}')
    return parse_response(r, validate=self.validate(validate))
