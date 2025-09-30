from typing_extensions import Literal, overload
from dataclasses import dataclass
from datetime import datetime

from dydx.core import timestamp as ts, TypedDict
from dydx.core.types import PerpetualPosition, PerpetualPositionStatus
from .core import IndexerMixin, response_parser, Response

class PositionsResponse(TypedDict):
  positions: list[PerpetualPosition]

parse_response = response_parser(PositionsResponse)

@dataclass
class ListPositions(IndexerMixin):
  @overload
  async def list_positions(
    self, address: str, *,
    subaccount: int = 0,
    status: PerpetualPositionStatus | None = None,
    limit: int | None = None,
    end_height: int | None = None,
    end: datetime | None = None,
    validate: bool | None = None,
    unsafe: Literal[True],
  ) -> PositionsResponse:
    ...
  @overload
  async def list_positions(
    self, address: str, *,
    subaccount: int = 0,
    status: PerpetualPositionStatus | None = None,
    limit: int | None = None,
    end_height: int | None = None,
    end: datetime | None = None,
    validate: bool | None = None,
  ) -> Response[PositionsResponse]:
    ...
  async def list_positions(
    self, address: str, *,
    subaccount: int = 0,
    status: PerpetualPositionStatus | None = None,
    limit: int | None = None,
    end_height: int | None = None,
    end: datetime | None = None,
    validate: bool | None = None,
    unsafe: bool = False,
  ) -> Response[PositionsResponse] | PositionsResponse:
    """Retrieves perpetual positions for a specific subaccount. Both open and closed/historical positions can be queried.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `status`: Status filter.
    - `limit`: Maximum number of perpetual positions to return in the response.
    - `end_height`: Restricts results to positions created at or before a specific blockchain height.
    - `end`: 	Restricts results to positions created at or before a specific timestamp.
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

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
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))