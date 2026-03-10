from dataclasses import dataclass

from dydx.core import TypedDict
from dydx.indexer.types import Subaccount
from .core import IndexerMixin, response_parser

class SubaccountResponse(TypedDict):
  subaccount: Subaccount

parse_response = response_parser(SubaccountResponse)

@dataclass
class GetSubaccount(IndexerMixin):
  async def get_subaccount(
    self, address: str, *,
    subaccount: int = 0,
    validate: bool | None = None,
  ) -> Subaccount:
    """Retrieves a specific subaccount associated with a given address and subaccount number.

    - `address`: The address of the subaccount.
    - `subaccount`: The subaccount number.
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-subaccount)
    """
    params = {}
    r = await self.request('GET', f'/v4/addresses/{address}/subaccountNumber/{subaccount}', params=params)
    return parse_response(r, validate=self.validate(validate))['subaccount']