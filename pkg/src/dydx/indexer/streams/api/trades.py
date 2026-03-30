from typing_extensions import AsyncIterable, Literal, TypedDict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import pydantic

from typed_core.util import Stream
from ..core import StreamsMixin, Unsubscribed

class Trade(TypedDict):
  id: str
  side: Literal['BUY', 'SELL']
  size: Decimal
  price: Decimal
  type: Literal['LIMIT', 'LIQUIDATED', 'DELEVERAGED']
  createdAt: datetime
  createdAtHeight: str

class TradeUpdate(TypedDict):
  id: str
  createdAt: datetime
  side: Literal['BUY', 'SELL']
  price: Decimal
  size: Decimal
  type: Literal['LIMIT', 'LIQUIDATED', 'DELEVERAGED']

class Reply(TypedDict):
  trades: list[Trade]

class Notification(TypedDict):
  trades: list[TradeUpdate]

reply_adapter = pydantic.TypeAdapter(Reply)
notification_adapter = pydantic.TypeAdapter(Notification)

@dataclass
class Trades(StreamsMixin):
  async def trades(
    self, *, id: str, batched: bool = True, validate: bool | None = None,
  ) -> Stream[Notification, Reply, Unsubscribed]:
    """
    Subscribe to the indexer trades feed for a market.

    - `id`: Market ticker.
    - `batched`: Reduce incoming messages by batching contents.
    - `validate`: Whether to validate reply and update payloads against the generated schemas.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/websockets#trades)
    """
    stream = await self.client.subscribe(f'v4_trades:{id}', {'batched': batched})

    async def parsed_stream() -> AsyncIterable[Notification]:
      async for msg in stream:
        data = msg['contents']
        msgs: list[Notification] = data if batched else [data]
        for d in msgs:
          yield notification_adapter.validate_python(d) if self.validate(validate) else d

    c = stream.reply['contents']
    reply: Reply = reply_adapter.validate_python(c) if self.validate(validate) else c
    return Stream(reply, parsed_stream(), stream.unsubscribe)

