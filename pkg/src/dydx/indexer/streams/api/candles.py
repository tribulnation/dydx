from typing_extensions import AsyncIterable, Literal, NotRequired, TypedDict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import pydantic

from typed_core.util import Stream
from ..core import StreamsMixin, Unsubscribed

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

class Notification(TypedDict):
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

class Reply(TypedDict):
  candles: list[Candle]

reply_adapter = pydantic.TypeAdapter(Reply)
notification_adapter = pydantic.TypeAdapter(Notification)

@dataclass
class Candles(StreamsMixin):
  async def raw_candles(
    self, *, id: str, batched: bool = True, validate: bool | None = None,
  ) -> Stream[Notification, Reply, Unsubscribed]:
    """
    Subscribe to the indexer candles feed for a market and resolution.

    - `id`: Market and candle resolution formatted as {market}/{resolution}.
    - `batched`: Reduce incoming messages by batching contents.
    - `validate`: Whether to validate reply and update payloads against the generated schemas.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/websockets#candles)
    """
    stream = await self.client.subscribe(f'v4_candles:{id}', {'batched': batched})

    async def parsed_stream() -> AsyncIterable[Notification]:
      async for msg in stream:
        data = msg['contents']
        msgs: list[Notification] = data if batched else [data]
        for d in msgs:
          yield notification_adapter.validate_python(d) if self.validate(validate) else d

    c = stream.reply['contents']
    reply: Reply = reply_adapter.validate_python(c) if self.validate(validate) else c
    return Stream(reply, parsed_stream(), stream.unsubscribe)

