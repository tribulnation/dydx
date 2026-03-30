from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing_extensions import Literal, TypedDict
from ..core import IndexerMixin, response_parser

class PnlTick(TypedDict):
  blockHeight: str
  blockTime: datetime
  createdAt: datetime
  equity: Decimal
  totalPnl: Decimal
  netTransfer: Decimal

class VaultHistoricalPnl(TypedDict):
  ticker: str
  historicalPnl: PnlTick

parse_response = response_parser(list[VaultHistoricalPnl])

@dataclass
class GetVaultsHistoricalPnl(IndexerMixin):
  async def get_vaults_historical_pnl(
    self,
    *,
    resolution: Literal['hour', 'day'],
    validate: bool | None = None
  ) -> list[VaultHistoricalPnl]:
    """
    Get vaults historical pnl

    - `resolution`: PnL tick resolution.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/vaults#get-vaults-historical-pnl)
    """
    params: dict[str, object] = {
      'resolution': resolution,
    }
    r = await self.request('GET', '/v4/vault/v1/vaults/historicalPnl', params=params)
    return parse_response(r, validate=self.validate(validate))

