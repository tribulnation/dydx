from typing_extensions import AsyncIterable
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from dydx.core import timestamp as ts, TypedDict
from dydx.indexer.types import PositionSide
from .core import IndexerMixin, response_parser

class FundingPayment(TypedDict):
  createdAt: datetime
  createdAtHeight: int
  perpetualId: str
  ticker: str
  oraclePrice: Decimal
  size: Decimal
  side: PositionSide
  rate: Decimal
  payment: Decimal
  subaccountNumber: int
  fundingIndex: Decimal

class FundingPayments(TypedDict):
  fundingPayments: list[FundingPayment]

parse_response = response_parser(FundingPayments)

@dataclass
class GetFundingPayments(IndexerMixin):
  async def get_funding_payments(
    self, address: str, *,
    subaccount: int = 0,
    ticker: str | None = None,
    start: datetime | None = None,
    limit: int | None = None,
    page: int | None = None,
    validate: bool | None = None,
  ) -> list[FundingPayment]:
    """Retrieves funding payment history for a specific subaccount. Funding payments are periodic settlements that occur between long and short positions based on the funding rate.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `ticker`: The market ticker (e.g. `'BTC-USD'`).
    - `start`: If given, fetches funding payments starting from the given timestamp.
    - `limit`: The max. number of funding payments to retrieve.
    - `page`: 	The page number for paginated results (default: 1).
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-funding-payments)
    """
    params = {'address': address, 'subaccountNumber': subaccount}
    if ticker is not None:
      params['ticker'] = ticker
    if start is not None:
      params['afterOrAt'] = ts.dump(start)
    if limit is not None:
      params['limit'] = limit
    if page is not None:
      params['page'] = page
    r = await self.request('GET', '/v4/fundingPayments', params=params)
    return parse_response(r, validate=self.validate(validate))['fundingPayments']

  
  async def get_funding_payments_paged(
    self, address: str, *,
    subaccount: int = 0,
    ticker: str | None = None,
    start: datetime | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> AsyncIterable[list[FundingPayment]]:
    """Retrieves funding payment history for a specific subaccount. Funding payments are periodic settlements that occur between long and short positions based on the funding rate.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `ticker`: The market ticker (e.g. `'BTC-USD'`).
    - `start`: If given, fetches funding payments starting from the given timestamp.
    - `limit`: The max. number of funding payments to retrieve.
    - `page`: 	The page number for paginated results (default: 1).
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-funding-payments)
    """
    page = 1
    while True:
      funding_payments = await self.get_funding_payments(address, subaccount=subaccount, ticker=ticker, start=start, limit=limit, page=page, validate=validate)
      if not funding_payments:
        break
      yield funding_payments
      page += 1