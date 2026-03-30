from typing_extensions import AsyncIterable, Literal, NotRequired, TypedDict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import pydantic

from typed_core.util import Stream
from ..core import StreamsMixin, Unsubscribed

class OraclePriceMarket(TypedDict):
  oraclePrice: Decimal
  effectiveAt: datetime
  effectiveAtHeight: str
  marketId: int

class PerpetualMarket(TypedDict):
  clobPairId: str
  ticker: str
  status: Literal['ACTIVE', 'PAUSED', 'CANCEL_ONLY', 'POST_ONLY', 'INITIALIZING', 'FINAL_SETTLEMENT']
  oraclePrice: NotRequired[Decimal | None]
  priceChange24H: Decimal
  volume24H: Decimal
  trades24H: int
  nextFundingRate: Decimal
  initialMarginFraction: Decimal
  maintenanceMarginFraction: Decimal
  openInterest: Decimal
  atomicResolution: int
  quantumConversionExponent: int
  tickSize: Decimal
  stepSize: Decimal
  stepBaseQuantums: int
  subticksPerTick: int
  marketType: Literal['CROSS', 'ISOLATED']
  openInterestLowerCap: NotRequired[Decimal | None]
  openInterestUpperCap: NotRequired[Decimal | None]
  baseOpenInterest: Decimal
  defaultFundingRate1H: NotRequired[Decimal | None]

class TradingPerpetualMarket(TypedDict):
  atomicResolution: NotRequired[int|None]
  baseAsset: NotRequired[str|None]
  baseOpenInterest: NotRequired[Decimal|None]
  basePositionSize: NotRequired[Decimal|None]
  clobPairId: NotRequired[str|None]
  id: NotRequired[str|None]
  incrementalPositionSize: NotRequired[Decimal|None]
  initialMarginFraction: NotRequired[Decimal|None]
  maintenanceMarginFraction: NotRequired[Decimal|None]
  marketId: NotRequired[int|None]
  marketType: NotRequired[Literal['PERPETUAL', 'SPOT']|None]
  maxPositionSize: NotRequired[Decimal|None]
  nextFundingRate: NotRequired[Decimal|None]
  openInterest: NotRequired[Decimal|None]
  oraclePrice: NotRequired[Decimal | None]
  priceChange24H: NotRequired[Decimal|None]
  quantumConversionExponent: NotRequired[int|None]
  quoteAsset: NotRequired[str|None]
  status: NotRequired[Literal['ACTIVE', 'PAUSED', 'CANCEL_ONLY', 'POST_ONLY', 'INITIALIZING', 'FINAL_SETTLEMENT']|None]
  stepBaseQuantums: NotRequired[int|None]
  stepSize: NotRequired[Decimal|None]
  subticksPerTick: NotRequired[int|None]
  tickSize: NotRequired[Decimal|None]
  ticker: NotRequired[str|None]
  trades24H: NotRequired[int|None]
  volume24H: NotRequired[Decimal|None]

class Reply(TypedDict):
  markets: dict[str, PerpetualMarket]

class Notification(TypedDict):
  trading: NotRequired[dict[str, TradingPerpetualMarket]|None]
  oraclePrices: NotRequired[dict[str, OraclePriceMarket]|None]

reply_adapter = pydantic.TypeAdapter(Reply)
notification_adapter = pydantic.TypeAdapter(Notification)

@dataclass
class Markets(StreamsMixin):
  async def markets(
    self, *, batched: bool = True, validate: bool | None = None,
  ) -> Stream[Notification, Reply, Unsubscribed]:
    """
    Subscribe to the indexer markets feed.

    - `batched`: Reduce incoming messages by batching contents.
    - `validate`: Whether to validate reply and update payloads against the generated schemas.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/websockets#markets)
    """
    stream = await self.client.subscribe('v4_markets', {'batched': batched})

    async def parsed_stream() -> AsyncIterable[Notification]:
      async for msg in stream:
        data = msg['contents']
        msgs: list[Notification] = data if batched else [data]
        for d in msgs:
          yield notification_adapter.validate_python(d) if self.validate(validate) else d

    c = stream.reply['contents']
    reply: Reply = reply_adapter.validate_python(c) if self.validate(validate) else c
    return Stream(reply, parsed_stream(), stream.unsubscribe)

