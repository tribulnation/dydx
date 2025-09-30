from typing_extensions import Literal, overload
from dataclasses import dataclass

from dydx.core import TypedDict
from dydx.core.types import PerpetualPosition, AssetPosition
from .core import IndexerMixin, response_parser, Response

class Subaccount(TypedDict):
  address: str
  subaccountNumber: int
  equity: str
  freeCollateral: str
  openPerpetualPositions: dict[str, PerpetualPosition]
  assetPositions: dict[str, AssetPosition]
  marginEnabled: bool
  updatedAtHeight: str
  latestProcessedBlockHeight: str

class Subaccounts(TypedDict):
  subaccounts: list[Subaccount]

parse_response = response_parser(Subaccounts)

@dataclass
class GetSubaccounts(IndexerMixin):
  @overload
  async def get_subaccounts(
    self, address: str, *,
    limit: int | None = None,
    validate: bool | None = None,
    unsafe: Literal[True] = True,
  ) -> Subaccounts:
    ...
  @overload
  async def get_subaccounts(
    self, address: str, *,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> Response[Subaccounts]:
    ...
  async def get_subaccounts(
    self, address: str, *,
    limit: int | None = None,
    validate: bool | None = None,
    unsafe: bool = False,
  ) -> Response[Subaccounts] | Subaccounts:
    """Retrieves a list of subaccounts associated with a given address. Subaccounts are related addresses that fall under the authority or ownership of the primary address.

    - `address`: The address of the subaccount.
    - `limit`: The max. number of subaccounts to retrieve.
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-subaccounts)
    """
    params = {}
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', f'/v4/addresses/{address}', params=params)
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))