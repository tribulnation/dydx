from typing_extensions import Any, TypeVar, Generic
from abc import abstractmethod
from dataclasses import dataclass, field
import asyncio

from .base import RpcSocketClient

M = TypeVar('M', default=Any)
R = TypeVar('R', default=Any)

@dataclass
class MultiplexRpcSocketClient(RpcSocketClient[M, R], Generic[M, R]):
  """Multiplexed request/response socket client. It uses IDs to identify requests and responses."""
  replies: dict[int, asyncio.Future[R]] = field(default_factory=dict)
  counter: int = 0

  @abstractmethod
  def parse_response(self, msg: str | bytes) -> tuple[int, R]:
    ...

  def on_msg(self, msg: str | bytes):
    id, result = self.parse_response(msg)
    self.replies[id].set_result(result)

  @abstractmethod
  async def send(self, id: int, msg: M):
    ...

  async def request(self, msg: M) -> R:
    id = self.counter
    self.counter += 1
    self.replies[id] = asyncio.Future()
    await self.send(id, msg)
    res = await self.wait_with_listener(self.replies[id])
    del self.replies[id]
    return res
