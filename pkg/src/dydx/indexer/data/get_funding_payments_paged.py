from typing_extensions import AsyncIterable
from dataclasses import dataclass
from datetime import datetime

from typed_core import PaginatedResponse
from .api.get_funding_payments import GetFundingPayments, FundingPayment

@dataclass
class GetFundingPaymentsPaged(GetFundingPayments):
  def get_funding_payments_paged(
    self,
    address: str,
    *,
    subaccount: int,
    ticker: str | None = None,
    after_or_at: datetime | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> PaginatedResponse[FundingPayment, int]:
    """Retrieves funding payment history for a specific subaccount. Funding payments are periodic settlements that occur between long and short positions based on the funding rate.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `ticker`: The market ticker (e.g. `'BTC-USD'`).
    - `after_or_at`: If given, fetches funding payments starting from the given timestamp.
    - `limit`: The max. number of funding payments to retrieve.
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-funding-payments)
    """
    async def next(page: int) -> tuple[list[FundingPayment], int | None]:
      response = await self.get_funding_payments(
        address,
        subaccount=subaccount,
        ticker=ticker,
        after_or_at=after_or_at,
        limit=limit,
        page=page,
        validate=validate,
      )
      funding_payments = response['fundingPayments']
      next_page = page + 1 if len(funding_payments) == limit else None
      return funding_payments, next_page

    return PaginatedResponse(1, next)
