from typing_extensions import Any, TypeVar, Generic, Literal, TypedDict, AsyncIterable
from abc import abstractmethod
from dataclasses import dataclass, field
import asyncio

from dydx.core import UserError
from .base import RpcSocketClient

M = TypeVar('M', default=Any)
R = TypeVar('R', default=Any)
S = TypeVar('S', default=Any)
D = TypeVar('D', default=Any)

class Response(TypedDict, Generic[R]):
  kind: Literal['response']
  response: R

class Subscription(TypedDict, Generic[D]):
  kind: Literal['subscription']
  channel: str
  data: D

Message = Response[R] | Subscription[D]

@dataclass
class StreamsRPCSocketClient(RpcSocketClient[M, R], Generic[M, R, S, D]):
  lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False, repr=False)
  replies: asyncio.Queue[R] = field(default_factory=asyncio.Queue, init=False, repr=False)
  subscribers: dict[str, asyncio.Queue[D]] = field(default_factory=dict, init=False, repr=False)

  @abstractmethod
  async def req_subscription(self, channel: str, *, id: str | None = None, batched: bool | None = None) -> S:
    ...

  @abstractmethod
  async def req_unsubscription(self, channel: str):
    ...

  @abstractmethod
  def parse_msg(self, msg: str | bytes) -> Message[R, D] | None:
    ...

  def on_msg(self, msg: str | bytes):
    obj = self.parse_msg(msg)
    if obj is None:
      return
    elif obj['kind'] == 'response':
      self.replies.put_nowait(obj['response'])
    elif obj['kind'] == 'subscription':
      if (q := self.subscribers.get(obj['channel'])) is not None:
        q.put_nowait(obj['data'])

  @abstractmethod
  async def send(self, msg: M):
    ...

  async def request(self, msg: M) -> R:
    async with self.lock:
      await self.send(msg)
      return await self.replies.get()

  async def subscribe(self, channel: str, *, id: str | None = None, batched: bool | None = None) -> tuple[S, AsyncIterable[D]]:
    if channel in self.subscribers:
      raise UserError(f'Channel {channel} already subscribed')

    self.subscribers[channel] = asyncio.Queue()
    r = await self.req_subscription(channel, id=id, batched=batched)

    async def gen():
      while True:
        if (q := self.subscribers.get(channel)) is None:
          break # channel unsubscribed
        yield await self.wait_with_listener(q.get())

    return r, gen()

  async def unsubscribe(self, channel: str):
    if channel not in self.subscribers:
      raise UserError(f'Channel {channel} not subscribed')
    del self.subscribers[channel]
    await self.req_unsubscription(channel)

    