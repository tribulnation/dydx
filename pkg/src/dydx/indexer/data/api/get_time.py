from dataclasses import dataclass
from datetime import datetime
from typing_extensions import TypedDict
from ..core import IndexerMixin, response_parser

class TimeResponse(TypedDict):
  iso: datetime
  epoc: float

parse_response = response_parser(TimeResponse)

@dataclass
class GetTime(IndexerMixin):
  async def get_time(
    self,
    validate: bool | None = None
  ) -> TimeResponse:
    """
    Get time

    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/utility#get-time)
    """
    r = await self.request('GET', '/v4/time')
    return parse_response(r, validate=self.validate(validate))

