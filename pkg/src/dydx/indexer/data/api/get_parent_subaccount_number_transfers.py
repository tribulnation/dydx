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
class GetParentSubaccountTransfers(IndexerMixin):
  async def get_parent_subaccount_transfers(
    self,
    address: str,
    *,
    parent_subaccount: int,
    limit: int | None = None,
    created_before_or_at_height: int | None = None,
    created_before_or_at: datetime | None = None,
    page: int | None = None,
    validate: bool | None = None
  ) -> TransfersResponse:
    """
    Get parent subaccount transfers

    - `address`: Wallet address that owns the account.
    - `parent_subaccount`: Parent subaccount number.
    - `limit`: Maximum number of results to return.
    - `created_before_or_at_height`: Restrict results to entries created at or before a specific block height.
    - `created_before_or_at`: Restrict results to entries created at or before a specific timestamp.
    - `page`: Page number for paginated results.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/accounts#get-parent-subaccount-number-transfers)
    """
    params: dict[str, object] = {
      'address': address,
      'parentSubaccountNumber': parent_subaccount,
    }
    if limit is not None:
      params['limit'] = limit
    if created_before_or_at_height is not None:
      params['createdBeforeOrAtHeight'] = created_before_or_at_height
    if created_before_or_at is not None:
      params['createdBeforeOrAt'] = ts.dump(created_before_or_at)
    if page is not None:
      params['page'] = page
    r = await self.request('GET', '/v4/transfers/parentSubaccountNumber', params=params)
    return parse_response(r, validate=self.validate(validate))
