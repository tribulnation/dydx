from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from dydx.core import timestamp as ts
from typing_extensions import Literal, NotRequired, TypedDict
from ..core import IndexerMixin, response_parser

class Account(TypedDict):
  address: str
  subaccountNumber: NotRequired[int|None]

class Transfer(TypedDict):
  id: str
  sender: Account
  recipient: Account
  size: Decimal
  createdAt: datetime
  createdAtHeight: str
  symbol: str
  type: Literal['TRANSFER_IN', 'TRANSFER_OUT', 'DEPOSIT', 'WITHDRAWAL']
  transactionHash: str

class TransfersResponse(TypedDict):
  transfers: list[Transfer]

parse_response = response_parser(TransfersResponse)

@dataclass
class GetTransfers(IndexerMixin):
  async def get_transfers(
    self,
    address: str,
    *,
    subaccount: int,
    created_before_or_at_height: int | None = None,
    created_before_or_at: datetime | None = None,
    limit: int | None = None,
    page: int | None = None,
    validate: bool | None = None
  ) -> TransfersResponse:
    """
    Retrieve transfer history for a subaccount.

    - `address`: Wallet address that owns the subaccount.
    - `subaccount`: Subaccount number.
    - `created_before_or_at_height`: Latest block height to include.
    - `created_before_or_at`: Latest timestamp to include.
    - `limit`: Maximum number of transfers to return.
    - `page`: Page number for paginated results.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http#get-transfers)
    """
    params: dict[str, object] = {
      'address': address,
      'subaccountNumber': subaccount,
    }
    if created_before_or_at_height is not None:
      params['createdBeforeOrAtHeight'] = created_before_or_at_height
    if created_before_or_at is not None:
      params['createdBeforeOrAt'] = ts.dump(created_before_or_at)
    if limit is not None:
      params['limit'] = limit
    if page is not None:
      params['page'] = page
    r = await self.request('GET', '/v4/transfers', params=params)
    return parse_response(r, validate=self.validate(validate))
