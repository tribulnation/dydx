from typing_extensions import AsyncIterable, TypedDict
from dataclasses import dataclass
from datetime import datetime
import pydantic

from typed_core.util import Stream
from ..core import StreamsMixin, Unsubscribed

class Reply(TypedDict):
  height: str
  time: datetime

class Notification(TypedDict):
  blockHeight: str
  time: datetime

reply_adapter = pydantic.TypeAdapter(Reply)
notification_adapter = pydantic.TypeAdapter(Notification)

@dataclass
class BlockHeight(StreamsMixin):
  async def block_height(
    self, *, batched: bool = True, validate: bool | None = None
  ) -> Stream[Notification, Reply, Unsubscribed]:
    """
    Subscribe to the indexer block height feed.

    - `batched`: Reduce incoming messages by batching contents.
    - `validate`: Whether to validate reply and update payloads against the generated schemas.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/websockets#block-height)
    """
    stream = await self.client.subscribe('v4_block_height', {'batched': batched})

    async def parsed_stream() -> AsyncIterable[Notification]:
      async for msg in stream:
        data = msg['contents']
        msgs: list[Notification] = data if batched else [data]
        for d in msgs:
          yield notification_adapter.validate_python(d) if self.validate(validate) else d

    c = stream.reply['contents']
    reply: Reply = reply_adapter.validate_python(c) if self.validate(validate) else c
    return Stream(reply, parsed_stream(), stream.unsubscribe)

