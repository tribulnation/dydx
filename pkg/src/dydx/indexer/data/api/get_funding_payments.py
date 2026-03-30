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
class GetFundingPayments(IndexerMixin):
  async def get_funding_payments(
    self,
    address: str,
    *,
    subaccount: int,
    ticker: str | None = None,
    after_or_at: datetime | None = None,
    limit: int | None = None,
    page: int | None = None,
    validate: bool | None = None
  ) -> FundingPaymentsResponse:
    """
    Retrieve funding payment history for a subaccount.

    - `address`: Wallet address that owns the subaccount.
    - `subaccount`: Subaccount number.
    - `ticker`: Market ticker filter.
    - `after_or_at`: Earliest timestamp to include.
    - `limit`: Maximum number of funding payments to return.
    - `page`: Page number for paginated results.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http#get-funding-payments)
    """
    params: dict[str, object] = {
      'address': address,
      'subaccountNumber': subaccount,
    }
    if ticker is not None:
      params['ticker'] = ticker
    if after_or_at is not None:
      params['afterOrAt'] = ts.dump(after_or_at)
    if limit is not None:
      params['limit'] = limit
    if page is not None:
      params['page'] = page
    r = await self.request('GET', '/v4/fundingPayments', params=params)
    return parse_response(r, validate=self.validate(validate))
