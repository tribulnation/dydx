from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from dydx.core import timestamp as ts
from typing_extensions import Literal, TypedDict
from ..core import IndexerMixin, response_parser

class FundingPayment(TypedDict):
  createdAt: datetime
  createdAtHeight: str
  perpetualId: str
  ticker: str
  oraclePrice: Decimal
  size: Decimal
  side: Literal['LONG', 'SHORT']
  rate: Decimal
  payment: Decimal
  subaccountNumber: str
  fundingIndex: Decimal

class FundingPaymentsResponse(TypedDict):
  fundingPayments: list[FundingPayment]

parse_response = response_parser(FundingPaymentsResponse)

@dataclass
class GetFundingPaymentsForParentSubaccount(IndexerMixin):
  async def get_funding_payments_for_parent_subaccount(
    self,
    address: str,
    *,
    parent_subaccount: int,
    limit: int | None = None,
    after_or_at: datetime | None = None,
    page: int | None = None,
    validate: bool | None = None
  ) -> FundingPaymentsResponse:
    """
    Get funding payments for parent subaccount

    - `address`: Wallet address that owns the account.
    - `parent_subaccount`: Parent subaccount number.
    - `limit`: Maximum number of results to return.
    - `after_or_at`: Only include payments created at or after this timestamp.
    - `page`: Page number for paginated results.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http/accounts#get-funding-payments-for-parent-subaccount)
    """
    params: dict[str, object] = {
      'address': address,
      'parentSubaccountNumber': parent_subaccount,
    }
    if limit is not None:
      params['limit'] = limit
    if after_or_at is not None:
      params['afterOrAt'] = ts.dump(after_or_at)
    if page is not None:
      params['page'] = page
    r = await self.request('GET', '/v4/fundingPayments/parentSubaccount', params=params)
    return parse_response(r, validate=self.validate(validate))
