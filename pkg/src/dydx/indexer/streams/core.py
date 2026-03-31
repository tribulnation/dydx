from typing_extensions import Literal, Any, NotRequired, TypedDict
from dataclasses import dataclass, field
import asyncio
import logging
import orjson
import pydantic

from typed_core import LogicError, BadRequest
from typed_core.ws.streams import Streams, Subscription

logger = logging.getLogger('dydx.indexer.streams')

INDEXER_WS_URL = 'wss://indexer.dydx.trade/v4/ws'
INDEXER_TESTNET_WS_URL = 'wss://indexer.v4testnet.dydx.exchange/v4/ws'

class BaseMessage(TypedDict):
  connection_id: str
  message_id: int

class Connected(BaseMessage):
  type: Literal['connected']

class Channel(TypedDict):
  channel: str
  id: NotRequired[str]

class Subscribed(BaseMessage, Channel):
  type: Literal['subscribed']
  contents: Any

class Unsubscribed(BaseMessage, Channel):
  type: Literal['unsubscribed']

class Error(BaseMessage):
  type: Literal['error']

class Notification(BaseMessage, Channel):
  type: Literal['channel_data', 'channel_batch_data']
  version: str
  contents: Any

Msg = Connected | Subscribed | Unsubscribed | Error | Notification
MsgT: type[Msg] = Msg # type: ignore

msg_adapter = pydantic.TypeAdapter(MsgT)

class Params(TypedDict, total=False):
  batched: bool

def parse_channel_id(channel_id: str) -> tuple[str, str|None]:
  if ':' in channel_id:
    channel, id = channel_id.split(':')
    return channel, id
  else:
    return channel_id, None

def channel_id(msg: Channel) -> str:
  out = msg['channel']
  if (id := msg.get('id')) is not None and id != msg['channel']: # yes that happens, it's a dydx bug
    out += f':{id}'
  return out

@dataclass
class StreamsClient(Streams[Notification, Params, Subscribed, Unsubscribed]):
  url: str = INDEXER_WS_URL
  lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False, repr=False)
  replies: asyncio.Queue[Error | Subscribed | Unsubscribed] = field(default_factory=asyncio.Queue)

  def parse_msg(self, msg: str | bytes) -> Subscription | None:
    obj = msg_adapter.validate_json(msg)
    match obj['type']:
      case 'subscribed' | 'unsubscribed' | 'error':
        self.replies.put_nowait(obj)
      case 'channel_data' | 'channel_batch_data':
        channel = channel_id(obj)
        return {'channel': channel, 'notification': obj}

  async def send(self, msg):
    ws = await self.ws
    await ws.send(orjson.dumps(msg), text=True)

  async def request(self, msg):
    async with self.lock:
      await self.send(msg)
      return await self.replies.get()

  async def request_subscription(self, channel: str, params: Params | None = None) -> Subscribed:
    channel, id = parse_channel_id(channel)
    msg: dict = {
      'type': 'subscribe',
      'channel': channel,
    }
    if (params or {}).get('batched', False):
      msg['batched'] = True
    if id is not None:
      msg['id'] = id
    reply = await self.request(msg)
    if reply['type'] == 'error':
      raise BadRequest(reply)
    elif reply['type'] != 'subscribed':
      raise LogicError(f'Unexpected response type: {reply}')
    return reply

  async def request_unsubscription(self, channel: str, params: Params | None = None) -> Unsubscribed:
    channel, id = parse_channel_id(channel)
    msg = {
      'type': 'unsubscribe',
      'channel': channel,
    }
    if id is not None:
      msg['id'] = id
    reply = await self.request(msg)
    if reply['type'] == 'error':
      raise BadRequest(reply)
    if reply['type'] != 'unsubscribed':
      raise LogicError(f'Unexpected response type: {reply}')
    return reply

@dataclass(kw_only=True)
class StreamsMixin:
  client: StreamsClient = field(default_factory=StreamsClient)
  default_validate: bool = True

  def validate(self, validate: bool | None = None) -> bool:
    return self.default_validate if validate is None else validate

  async def __aenter__(self):
    await self.client.__aenter__()
    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.client.__aexit__(exc_type, exc_value, traceback)

  @classmethod
  def new(cls, url: str = INDEXER_WS_URL, *, validate: bool = True):
    return cls(client=StreamsClient(url=url), default_validate=validate)