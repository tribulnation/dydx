from typing_extensions import Any, AsyncIterable, NotRequired, TypedDict, NamedTuple
from dataclasses import dataclass
from decimal import Decimal
import pydantic

from typed_core.util import Stream
from ..core import StreamsMixin, Unsubscribed

class BookEntry(TypedDict):
  price: Decimal
  size: Decimal

class NotificationEntry(NamedTuple):
  price: Decimal
  size: Decimal

class Notification(TypedDict):
  bids: NotRequired[list[NotificationEntry]]
  asks: NotRequired[list[NotificationEntry]]

class Reply(TypedDict):
  bids: list[BookEntry]
  asks: list[BookEntry]

reply_adapter = pydantic.TypeAdapter(Reply)
notification_adapter = pydantic.TypeAdapter(Notification)

@dataclass
class Orders(StreamsMixin):
  async def orders(
    self, *, id: str, batched: bool = True, validate: bool | None = None,
  ) -> Stream[Notification, Reply, Unsubscribed]:
    """
    Subscribe to the indexer order book feed for a market.

    - `id`: Market ticker.
    - `batched`: Reduce incoming messages by batching contents.
    - `validate`: Whether to validate reply and update payloads against the generated schemas.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/websockets#orders)
    """
    stream = await self.client.subscribe(f'v4_orderbook:{id}', {'batched': batched})

    async def parsed_stream() -> AsyncIterable[Notification]:
      async for msg in stream:
        data = msg['contents']
        msgs: list[Notification] = data if batched else [data]
        for d in msgs:
          yield notification_adapter.validate_python(d) if self.validate(validate) else d

    c = stream.reply['contents']
    reply: Reply = reply_adapter.validate_python(c) if self.validate(validate) else c
    return Stream(reply, parsed_stream(), stream.unsubscribe)

