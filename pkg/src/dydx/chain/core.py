"""Shared dYdX Chain gRPC primitives."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from functools import wraps
from types import TracebackType

from grpclib.client import Channel
from grpclib.const import Status
from grpclib.exceptions import GRPCError, ProtocolError, StreamTerminatedError
from typed_core.exceptions import NetworkError
from typing_extensions import ParamSpec, Self, TypeVar

# gRPC statuses that represent transport failures rather than API/business errors.
_NETWORK_STATUSES = frozenset({Status.UNAVAILABLE})

P = ParamSpec('P')
T = TypeVar('T')

def wrap_exceptions(fn: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
  """Map grpclib transport failures from a gRPC call to typed_core NetworkError.

  Transport-level failures (GOAWAY, HTTP/2 protocol errors, terminated streams, and
  gRPC unavailable/502 responses) are raised as NetworkError. Business/API errors,
  which arrive either in a successful response payload or as a non-transport GRPCError,
  are left untouched.
  """
  @wraps(fn)
  async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
    """Await the wrapped gRPC call, normalizing transport exceptions."""
    try:
      return await fn(*args, **kwargs)
    except (ProtocolError, StreamTerminatedError, ConnectionError, TimeoutError) as exc:
      raise NetworkError(str(exc)) from exc
    except GRPCError as exc:
      if exc.status in _NETWORK_STATUSES:
        raise NetworkError(str(exc)) from exc
      raise
  return wrapper

@dataclass(kw_only=True)
class GrpcClient:
  """Async gRPC transport that owns a lazily opened channel."""

  host: str = 'oegs.dydx.trade'
  port: int = 443
  ssl: bool = True
  _channel: Channel | None = field(default=None, init=False, repr=False)

  @property
  def channel(self) -> Channel:
    """Return the gRPC channel, creating it if needed."""
    if self._channel is None:
      self._channel = Channel(self.host, self.port, ssl=self.ssl)
    return self._channel

  async def __aenter__(self) -> Self:
    """Open the channel for an async client context."""
    self.channel
    return self

  async def __aexit__(
    self,
    exc_type: type[BaseException] | None,
    exc: BaseException | None,
    traceback: TracebackType | None,
  ):
    """Close the channel for an async client context."""
    self.close()

  def close(self):
    """Close the open channel if one was created."""
    if self._channel is not None:
      self._channel.close()
      self._channel = None

@dataclass(kw_only=True)
class GrpcEndpoint:
  """Base class for module adapters sharing a gRPC transport."""

  client: GrpcClient

  @property
  def channel(self) -> Channel:
    """Return the active shared gRPC channel."""
    return self.client.channel

@dataclass(kw_only=True)
class GrpcRouter:
  """Base class for clients composed from gRPC module adapters."""

  client: GrpcClient

  def __post_init__(self):
    """Instantiate annotated child adapters with the shared transport."""
    for name, cls in self.__annotations__.items():
      if isinstance(cls, type) and issubclass(cls, GrpcEndpoint | GrpcRouter):
        setattr(self, name, cls(client=self.client))

  async def __aenter__(self) -> Self:
    """Open the shared gRPC transport for an async context."""
    await self.client.__aenter__()
    return self

  async def __aexit__(
    self,
    exc_type: type[BaseException] | None,
    exc: BaseException | None,
    traceback: TracebackType | None,
  ):
    """Close the shared gRPC transport for an async context."""
    await self.client.__aexit__(exc_type, exc, traceback)
