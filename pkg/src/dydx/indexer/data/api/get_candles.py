from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from dydx.core import timestamp as ts
from typing_extensions import Literal, NotRequired, TypedDict
from ..core import IndexerMixin, response_parser

class Candle(TypedDict):
  startedAt: datetime
  ticker: str
  resolution: Literal['1MIN', '5MINS', '15MINS', '30MINS', '1HOUR', '4HOURS', '1DAY']
  low: Decimal
  high: Decimal
  open: Decimal
  close: Decimal
  baseTokenVolume: Decimal
  usdVolume: Decimal
  trades: int
  startingOpenInterest: Decimal
  orderbookMidPriceOpen: NotRequired[Decimal | None]
  orderbookMidPriceClose: NotRequired[Decimal | None]

class CandlesResponse(TypedDict):
  candles: list[Candle]

parse_response = response_parser(CandlesResponse)

@dataclass
class GetCandles(IndexerMixin):
  async def get_candles(
    self,
    market: str,
    *,
    resolution: Literal[
      '1MIN', '5MINS', '15MINS', '30MINS', '1HOUR', '4HOURS', '1DAY'
    ],
    from_iso: datetime | None = None,
    to_iso: datetime | None = None,
    limit: int | None = None,
    validate: bool | None = None
  ) -> CandlesResponse:
    """
    Retrieve candle data for a perpetual market.

    - `market`: Perpetual market ticker.
    - `resolution`: Candle resolution.
    - `from_iso`: Start timestamp in ISO 8601 format.
    - `to_iso`: End timestamp in ISO 8601 format.
    - `limit`: Maximum number of candles to return.
    - `validate`: Whether to validate the response against the generated schema.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/http#get-candles)
    """
    params: dict[str, object] = {
      'resolution': resolution,
    }
    if from_iso is not None:
      params['fromISO'] = ts.dump(from_iso)
    if to_iso is not None:
      params['toISO'] = ts.dump(to_iso)
    if limit is not None:
      params['limit'] = limit
    r = await self.request('GET', f'/v4/candles/perpetualMarkets/{market}', params=params)
    return parse_response(r, validate=self.validate(validate))

