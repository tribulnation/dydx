from typing_extensions import Any, TypeVar, Generic, Literal, TypedDict, AsyncIterable
from abc import abstractmethod
from dataclasses import dataclass, field
from collections import defaultdict
import asyncio

from .base import RpcSocketClient

M = TypeVar('M', default=Any)
R = TypeVar('R', default=Any)
S = TypeVar('S', default=Any)

class Response(TypedDict, Generic[R]):
  kind: Literal['response']
  response: R

class Subscription(TypedDict, Generic[S]):
  kind: Literal['subscription']
  channel: str
  data: S

Message = Response[R] | Subscription[S]

@dataclass
class StreamsRPCSocketClient(RpcSocketClient[M, R], Generic[M, R, S]):
  """Multiplexed streams socket client, allowing subscription to multiple channels. Also supports serial request/response communication, using a lock to serialize requests"""
  lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False)
  replies: asyncio.Queue[R] = field(default_factory=asyncio.Queue, init=False)
  subscribers: dict[str, list[asyncio.Queue[S]]] = field(default_factory=lambda: defaultdict(list), init=False)

  @abstractmethod
  async def req_subscription(self, channel: str, **kwargs):
    ...

  @abstractmethod
  async def req_unsubscription(self, channel: str):
    ...

  @abstractmethod
  def parse_msg(self, msg: str | bytes) -> Message[R, S] | None:
    ...

  def on_msg(self, msg: str | bytes):
    obj = self.parse_msg(msg)
    if obj is None:
      return
    elif obj['kind'] == 'response':
      self.replies.put_nowait(obj['response'])
    elif obj['kind'] == 'subscription':
      for q in self.subscribers[obj['channel']]:
        q.put_nowait(obj['data'])

  @abstractmethod
  async def send(self, msg: M):
    ...

  async def request(self, msg: M) -> R:
    async with self.lock:
      await self.send(msg)
      return await self.replies.get()

  async def subscribe(self, channel: str, *, id: str | None = None, batched: bool | None = None) -> AsyncIterable[S]:
    q = asyncio.Queue()
    self.subscribers[channel].append(q)
    await self.req_subscription(channel, id=id, batched=batched)
    while True:
      yield await self.wait_with_listener(q.get())

  async def unsubscribe(self, channel: str):
    del self.subscribers[channel]
    await self.req_unsubscription(channel)

    