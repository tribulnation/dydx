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

class VaultPosition(TypedDict):
  ticker: str
  assetPosition: AssetPosition
  perpetualPosition: PerpetualPosition
  equity: Decimal

parse_response = response_parser(list[VaultPosition])

@dataclass
class GetMegavaultPositions(IndexerMixin):
  async def get_megavault_positions(
    self,
    validate: bool | None = None
  ) -> list[VaultPosition]:
    """
    Get megavault positions

    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/vaults#get-megavault-positions)
    """
    r = await self.request('GET', '/v4/vault/v1/megavault/positions')
    return parse_response(r, validate=self.validate(validate))

