from dataclasses import dataclass
from decimal import Decimal
from typing_extensions import Literal, TypedDict
from ..core import IndexerMixin, response_parser

class AssetPosition(TypedDict):
  size: Decimal
  symbol: str
  side: Literal['LONG', 'SHORT']
  assetId: str
  subaccountNumber: int

parse_response = response_parser(list[AssetPosition])

@dataclass
class GetParentAssetPositions(IndexerMixin):
  async def get_parent_asset_positions(
    self,
    address: str,
    *,
    parent_subaccount: int,
    validate: bool | None = None
  ) -> list[AssetPosition]:
    """
    Get parent asset positions

    - `address`: Wallet address that owns the account.
    - `parent_subaccount`: Parent subaccount number.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/accounts#get-parent-asset-positions)
    """
    params: dict[str, object] = {
      'address': address,
      'parentSubaccountNumber': parent_subaccount,
    }
    r = await self.request('GET', '/v4/assetPositions/parentSubaccountNumber', params=params)
    return parse_response(r, validate=self.validate(validate))
