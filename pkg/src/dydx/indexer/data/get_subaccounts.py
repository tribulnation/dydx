
from dataclasses import dataclass

from dydx.core import TypedDict
from dydx.indexer.types import Subaccount
from .core import IndexerMixin, response_parser


class Subaccounts(TypedDict):
  subaccounts: list[Subaccount]

parse_response = response_parser(Subaccounts)

@dataclass
class GetSubaccounts(IndexerMixin):
  async def get_subaccounts(
    self, address: str, *,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> list[Subaccount]:
    """Retrieves a list of subaccounts associated with a given address. Subaccounts are related addresses that fall under the authority or ownership of the primary address.

    - `address`: The address of the subaccount.
    - `limit`: The max. number of subaccounts to retrieve.
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-subaccounts)
    """
    params = {}
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', f'/v4/addresses/{address}', params=params)
    return parse_response(r, validate=self.validate(validate))['subaccounts']