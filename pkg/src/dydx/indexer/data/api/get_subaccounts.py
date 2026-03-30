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

class AddressResponse(TypedDict):
  subaccounts: list[Subaccount]
  totalTradingRewards: Decimal

parse_response = response_parser(AddressResponse)

@dataclass
class GetSubaccounts(IndexerMixin):
  async def get_subaccounts(
    self,
    address: str,
    *,
    limit: int | None = None,
    validate: bool | None = None
  ) -> AddressResponse:
    """
    Retrieve subaccounts for an address.

    - `address`: Account address.
    - `limit`: Maximum number of subaccounts to return.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http#get-subaccounts)
    """
    params: dict[str, object] = {}
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', f'/v4/addresses/{address}', params=params)
    return parse_response(r, validate=self.validate(validate))
