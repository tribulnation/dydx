from typing_extensions import AsyncIterable
from dataclasses import dataclass
from datetime import datetime

from .api.get_transfers import GetTransfers, Transfer

@dataclass
class GetTransfersPaged(GetTransfers):
  async def get_transfers_paged(
    self,
    address: str,
    *,
    subaccount: int,
    created_before_or_at_height: int | None = None,
    created_before_or_at: datetime | None = None,
    limit: int | None = None,
    validate: bool | None = None,
  ) -> AsyncIterable[list[Transfer]]:
    """Retrieves the transfer history for a specific subaccount.

    - `address`: The wallet address that owns the account.
    - `subaccount`: The identifier for the specific subaccount within the wallet address.
    - `created_before_or_at_height`: If given, fetches transfers up to and including the given block height.
    - `created_before_or_at`: If given, fetches transfers up to and including the given timestamp.
    - `limit`: The max. number of transfers to retrieve (default: 1000, max: 1000).
    - `validate`: Whether to validate the response against the expected schema.

    > [dYdX API docs](https://docs.dydx.xyz/indexer-client/http#get-transfers)
    """
    page = 1
    while True:
      response = await self.get_transfers(
        address,
        subaccount=subaccount,
        created_before_or_at_height=created_before_or_at_height,
        created_before_or_at=created_before_or_at,
        limit=limit,
        page=page,
        validate=validate,
      )
      transfers = response['transfers']
      if not transfers:
        break
      yield transfers
      page += 1
