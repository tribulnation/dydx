from dataclasses import dataclass
from typing_extensions import TypedDict
from ..core import IndexerMixin, response_parser

class ComplianceResponse(TypedDict):
  restricted: bool
  reason: str

parse_response = response_parser(ComplianceResponse)

@dataclass
class GetScreen(IndexerMixin):
  async def get_screen(
    self,
    address: str,
    *,
    validate: bool | None = None
  ) -> ComplianceResponse:
    """
    Get screen

    - `address`: Wallet address to screen.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/utility#get-screen)
    """
    params: dict[str, object] = {
      'address': address,
    }
    r = await self.request('GET', '/v4/screen', params=params)
    return parse_response(r, validate=self.validate(validate))
