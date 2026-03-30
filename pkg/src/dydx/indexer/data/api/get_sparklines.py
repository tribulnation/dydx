from dataclasses import dataclass
from decimal import Decimal
from typing_extensions import Literal
from ..core import IndexerMixin, response_parser

Sparkline = dict[str, list[Decimal]]

parse_response = response_parser(Sparkline)

@dataclass
class GetSparklines(IndexerMixin):
  async def get_sparklines(
    self,
    *,
    time_period: Literal['OneDay', 'SevenDays'],
    validate: bool | None = None
  ) -> Sparkline:
    """
    Get sparklines

    - `time_period`: Sparkline time period.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/markets#get-sparklines)
    """
    params: dict[str, object] = {
      'timePeriod': time_period,
    }
    r = await self.request('GET', '/v4/sparklines', params=params)
    return parse_response(r, validate=self.validate(validate))

