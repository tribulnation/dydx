from typing_extensions import Literal, Any, NotRequired
from dataclasses import dataclass, field
import json
import logging

from dydx.core import ApiError, TypedDict, validator
from dydx.core.ws.streams_rpc import StreamsRPCSocketClient, Message

logger = logging.getLogger('dydx.indexer.streams')

INDEXER_WS_URL = 'wss://indexer.dydx.trade/v4/ws'

class BaseMessage(TypedDict):
  connection_id: str
  message_id: int

class Connected(BaseMessage):
  type: Literal['connected']

class Subscribed(BaseMessage):
  type: Literal['subscribed']
  channel: str
  id: NotRequired[str|None]
  contents: Any

class Unsubscribed(BaseMessage):
  type: Literal['unsubscribed']
  channel: str
  id: NotRequired[str|None]

class Error(BaseMessage):
  type: Literal['error']

class Data(BaseMessage):
  type: Literal['channel_data', 'channel_batch_data']
  id: NotRequired[str|None]
  channel: str
  version: str
  contents: Any

Reply = Subscribed | Unsubscribed | Error
Msg = Connected | Reply | Data

validate_message = validator(Msg)

@dataclass(kw_only=True)
class StreamsClient(StreamsRPCSocketClient[Any, Reply, Subscribed, Data]):
  url: str = INDEXER_WS_URL

  def parse_msg(self, msg: str | bytes) -> Message[Reply, Data] | None:
    obj = validate_message(msg)
    match obj['type']:
      case 'connected':
        logger.info('Connected')
      case 'channel_data' | 'channel_batch_data':
        return {'kind': 'subscription', 'channel': obj['channel'], 'data': obj}
      case _:
        return {'kind': 'response', 'response': obj}

  async def send(self, msg):
    ws = await self.ws
    await ws.send(json.dumps(msg))

  async def req_subscription(self, channel: str, **kwargs) -> Subscribed:
    r = await self.request({
      'type': 'subscribe',
      'channel': channel,
      **kwargs,
    })
    if r['type'] == 'error':
      raise ApiError(r)
    elif r['type'] != 'subscribed':
      raise ApiError(f'Unexpected response type: {r["type"]}', r)
    return r

  async def req_unsubscription(self, channel: str):
    await self.send({
      'type': 'unsubscribe',
      'channel': channel,
    })


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