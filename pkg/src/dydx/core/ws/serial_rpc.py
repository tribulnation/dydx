from typing_extensions import Any, TypeVar, Generic
from abc import abstractmethod
from dataclasses import dataclass, field
import asyncio

from .base import RpcSocketClient

M = TypeVar('M', default=Any)

@dataclass
class SerialRpcSocketClient(RpcSocketClient[M, str|bytes], Generic[M]):
  """Serial request/response socket client. It uses a lock to serialize requests and responses."""
  lock: asyncio.Lock = field(default_factory=asyncio.Lock)
  replies: asyncio.Queue[str|bytes] = field(default_factory=asyncio.Queue)

  def on_msg(self, msg: str | bytes):
    self.replies.put_nowait(msg)

  @abstractmethod
  async def send(self, msg: M):
    ...

  async def request(self, msg: M) -> str | bytes:
    async with self.lock:
      await self.send(msg)
      res = await self.replies.get()
      return res
