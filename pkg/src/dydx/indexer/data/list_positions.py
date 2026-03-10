from dataclasses import dataclass
from datetime import datetime

from dydx.core import timestamp as ts, TypedDict
from dydx.indexer.types import PerpetualPosition, PerpetualPositionStatus
from .core import IndexerMixin, response_parser

class PositionsResponse(TypedDict):
  positions: list[PerpetualPosition]

parse_response = response_parser(PositionsResponse)

@dataclass
class ListPositions(IndexerMixin):
  async def list_positions(
    self, address: str, *,
    subaccount: int = 0,
    status: PerpetualPositionStatus | None = None,
    limit: int | None = None,
    end_height: int | None = None,
    end: datetime | None = None,
    validate: bool | None = None,
  ) -> list[PerpetualPosition]:
    """Retrieves perpetual positions for a specific subaccount. Both open and closed/historical positions can be queried.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `status`: Status filter.
    - `limit`: Maximum number of perpetual positions to return in the response.
    - `end_height`: Restricts results to positions created at or before a specific blockchain height.
    - `end`: 	Restricts results to positions created at or before a specific timestamp.
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#list-positions)
    """
    params = {'address': address, 'subaccountNumber': subaccount}
    if status is not None:
      params['status'] = status
    if limit is not None:
      params['limit'] = limit
    if end_height is not None:
      params['createdBeforeOrAtHeight'] = end_height
    if end is not None:
      params['createdBeforeOrAt'] = ts.dump(end)
    r = await self.request('GET', '/v4/perpetualPositions', params=params)
    return parse_response(r, validate=self.validate(validate))['positions']

  
  async def get_open_position(
    self, market: str, *,
    address: str,
    subaccount: int = 0,
    validate: bool | None = None,
  ) -> PerpetualPosition | None:
    """Retrieves the open perpetual position for a specific subaccount."""
    positions = await self.list_positions(address, subaccount=subaccount, status='OPEN', validate=validate)
    for p in positions:
      if p['market'] == market:
        return p