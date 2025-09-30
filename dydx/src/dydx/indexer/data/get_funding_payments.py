from typing_extensions import Literal, overload, AsyncIterable, Sequence
from dataclasses import dataclass
from datetime import datetime

from dydx.core import timestamp as ts, TypedDict
from .core import IndexerMixin, response_parser, Response

class Payment(TypedDict):
  ...

class FundingPayments(TypedDict):
  fundingPayments: list[Payment]

parse_response = response_parser(FundingPayments)

@dataclass
class GetFundingPayments(IndexerMixin):
  @overload
  async def get_funding_payments(
    self, address: str, *,
    subaccount: int = 0,
    ticker: str | None = None,
    page: int | None = None,
    start: datetime | None = None,
    limit: int | None = None,
    validate: bool | None = None,
    unsafe: Literal[True] = True,
  ) -> FundingPayments:
    ...
  @overload
  async def get_funding_payments(
    self, address: str, *,
    subaccount: int = 0,
    ticker: str | None = None,
    start: datetime | None = None,
    page: int | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> Response[FundingPayments]:
    ...
  async def get_funding_payments(
    self, address: str, *,
    subaccount: int = 0,
    ticker: str | None = None,
    start: datetime | None = None,
    limit: int | None = None,
    page: int | None = None,
    validate: bool | None = None,
    unsafe: bool = False,
  ) -> Response[FundingPayments] | FundingPayments:
    """Retrieves funding payment history for a specific subaccount. Funding payments are periodic settlements that occur between long and short positions based on the funding rate.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `ticker`: The market ticker (e.g. `'BTC-USD'`).
    - `start`: If given, fetches funding payments starting from the given timestamp.
    - `limit`: The max. number of funding payments to retrieve.
    - `page`: 	The page number for paginated results (default: 1).
    - `validate`: Whether to validate the response against the expected schema.
    - `unsafe`: Whether to raise an exception in case of an error.

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
    return parse_response(r, unsafe=unsafe, validate=self.validate(validate))

  
  async def get_funding_payments_paged(
    self, address: str, *,
    subaccount: int = 0,
    ticker: str | None = None,
    start: datetime | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> AsyncIterable[list[Payment]]:
    page = 1
    while True:
      r = await self.get_funding_payments(address, subaccount=subaccount, ticker=ticker, start=start, limit=limit, page=page, validate=validate, unsafe=True)
      if not r['fundingPayments']:
        break
      yield r['fundingPayments']
      page += 1