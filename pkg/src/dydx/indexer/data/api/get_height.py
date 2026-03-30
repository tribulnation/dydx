from dataclasses import dataclass
from datetime import datetime
from typing_extensions import TypedDict
from ..core import IndexerMixin, response_parser

class HeightResponse(TypedDict):
  height: str
  time: datetime

parse_response = response_parser(HeightResponse)

@dataclass
class GetHeight(IndexerMixin):
  async def get_height(
    self,
    validate: bool | None = None
  ) -> HeightResponse:
    """
    Get height

    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/utility#get-height)
    """
    r = await self.request('GET', '/v4/height')
    return parse_response(r, validate=self.validate(validate))

