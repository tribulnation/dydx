from typing_extensions import AsyncIterable, Literal, NotRequired, TypedDict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import pydantic

from typed_core.util import Stream
from ..core import StreamsMixin, Unsubscribed

class Account(TypedDict):
  address: str
  subaccountNumber: NotRequired[int|None]

class AssetPosition(TypedDict):
  size: Decimal
  symbol: str
  side: Literal['LONG', 'SHORT']
  assetId: str
  subaccountNumber: int

class AssetPositionSubaccountMessage(TypedDict):
  address: str
  subaccountNumber: int
  positionId: str
  assetId: str
  symbol: str
  side: Literal['LONG', 'SHORT']
  size: Decimal

class FillSubaccountMessage(TypedDict):
  id: str
  subaccountId: str
  side: Literal['BUY', 'SELL']
  liquidity: Literal['MAKER', 'TAKER']
  type: Literal['LIMIT', 'LIQUIDATED', 'LIQUIDATION', 'DELEVERAGED', 'OFFSETTING']
  clobPairId: str
  size: Decimal
  price: Decimal
  quoteAmount: Decimal
  eventId: str
  transactionHash: str
  createdAt: datetime
  createdAtHeight: NotRequired[str | None]
  ticker: str
  orderId: NotRequired[str | None]
  clientMetadata: NotRequired[str | None]

class Order(TypedDict):
  id: str
  subaccountId: str
  clientId: str
  clobPairId: str
  side: Literal['BUY', 'SELL']
  size: Decimal
  totalFilled: Decimal
  price: Decimal
  type: Literal['LIMIT', 'MARKET', 'STOP_LIMIT', 'STOP_MARKET', 'TRAILING_STOP', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'HARD_TRADE', 'FAILED_HARD_TRADE', 'TRANSFER_PLACEHOLDER']
  status: Literal['OPEN', 'FILLED', 'CANCELED', 'BEST_EFFORT_CANCELED', 'UNTRIGGERED', 'BEST_EFFORT_OPENED', 'PENDING']
  timeInForce: Literal['GTT', 'IOC', 'FOK']
  reduceOnly: NotRequired[bool | None]
  orderFlags: str
  goodTilBlock: NotRequired[str | None]
  goodTilBlockTime: NotRequired[datetime | None]
  createdAtHeight: NotRequired[str | None]
  clientMetadata: NotRequired[str | None]
  triggerPrice: NotRequired[Decimal | None]
  postOnly: NotRequired[bool | None]
  ticker: str
  updatedAt: NotRequired[datetime | None]
  updatedAtHeight: NotRequired[str | None]
  subaccountNumber: int
  orderRouterAddress: NotRequired[str|None]
  builderFee: NotRequired[Decimal | None]
  feePpm: NotRequired[Decimal | None]

class OrderSubaccountMessage(TypedDict):
  id: str
  subaccountId: str
  clientId: str
  clobPairId: str
  side: Literal['BUY', 'SELL']
  size: Decimal
  ticker: NotRequired[str | None]
  price: NotRequired[Decimal | None]
  type: Literal['LIMIT', 'MARKET', 'STOP_LIMIT', 'STOP_MARKET', 'TRAILING_STOP', 'TAKE_PROFIT', 'TAKE_PROFIT_MARKET', 'HARD_TRADE', 'FAILED_HARD_TRADE', 'TRANSFER_PLACEHOLDER']
  timeInForce: Literal['GTT', 'IOC', 'FOK']
  postOnly: NotRequired[bool | None]
  reduceOnly: NotRequired[bool | None]
  status: Literal['OPEN', 'FILLED', 'CANCELED', 'BEST_EFFORT_CANCELED', 'UNTRIGGERED', 'BEST_EFFORT_OPENED', 'PENDING']
  orderFlags: NotRequired[str | None]
  totalFilled: NotRequired[Decimal | None]
  totalOptimisticFilled: NotRequired[Decimal | None]
  goodTilBlock: NotRequired[str | None]
  goodTilBlockTime: NotRequired[datetime | None]
  triggerPrice: NotRequired[Decimal | None]
  updatedAt: NotRequired[datetime | None]
  updatedAtHeight: NotRequired[str | None]
  removalReason: NotRequired[str | None]
  createdAtHeight: NotRequired[str | None]
  clientMetadata: NotRequired[str | None]
  subaccountNumber: NotRequired[int | None]
  orderRouterAddress: NotRequired[str | None]

class PerpetualPosition(TypedDict):
  market: str
  status: Literal['OPEN', 'CLOSED', 'LIQUIDATED']
  side: Literal['LONG', 'SHORT']
  size: Decimal
  maxSize: Decimal
  entryPrice: Decimal
  exitPrice: NotRequired[Decimal | None]
  realizedPnl: NotRequired[Decimal | None]
  unrealizedPnl: NotRequired[Decimal | None]
  createdAt: datetime
  createdAtHeight: str
  closedAt: NotRequired[datetime | None]
  sumOpen: Decimal
  sumClose: Decimal
  netFunding: Decimal
  subaccountNumber: int

class PerpetualPositionSubaccountMessage(TypedDict):
  market: str
  status: Literal['OPEN', 'CLOSED', 'LIQUIDATED']
  side: Literal['LONG', 'SHORT']
  size: Decimal
  maxSize: Decimal
  entryPrice: Decimal
  exitPrice: NotRequired[Decimal | None]
  realizedPnl: NotRequired[Decimal | None]
  unrealizedPnl: NotRequired[Decimal | None]
  createdAt: NotRequired[datetime | None]
  createdAtHeight: NotRequired[str | None]
  closedAt: NotRequired[datetime | None]
  sumOpen: Decimal
  sumClose: Decimal
  netFunding: Decimal
  subaccountNumber: int

class TradingRewardSubaccountMessage(TypedDict):
  tradingReward: Decimal
  createdAt: NotRequired[datetime | None]
  createdAtHeight: NotRequired[str | None]

AssetPositionsMap = dict[str, AssetPosition]

PerpetualPositionsMap = dict[str, PerpetualPosition]

class TransferSubaccountMessage(TypedDict):
  sender: Account
  recipient: Account
  symbol: str
  size: Decimal
  type: Literal['TRANSFER_IN', 'TRANSFER_OUT', 'DEPOSIT', 'WITHDRAWAL']
  transactionHash: str
  createdAt: NotRequired[datetime | None]
  createdAtHeight: NotRequired[str | None]

class Subaccount(TypedDict):
  address: str
  subaccountNumber: int
  equity: Decimal
  freeCollateral: Decimal
  openPerpetualPositions: PerpetualPositionsMap
  assetPositions: AssetPositionsMap
  marginEnabled: bool
  updatedAtHeight: str
  latestProcessedBlockHeight: str

class Notification(TypedDict):
  perpetualPositions: NotRequired[list[PerpetualPositionSubaccountMessage]|None]
  assetPositions: NotRequired[list[AssetPositionSubaccountMessage]|None]
  orders: NotRequired[list[OrderSubaccountMessage]|None]
  fills: NotRequired[list[FillSubaccountMessage]|None]
  transfers: NotRequired[list[TransferSubaccountMessage] | TransferSubaccountMessage|None]
  tradingReward: NotRequired[TradingRewardSubaccountMessage|None]
  tradingRewards: NotRequired[list[TradingRewardSubaccountMessage]|None]
  blockHeight: NotRequired[str | None]

class ParentSubaccount(TypedDict):
  address: str
  parentSubaccountNumber: int
  equity: Decimal
  freeCollateral: Decimal
  childSubaccounts: list[Subaccount]

class Reply(TypedDict):
  subaccount: ParentSubaccount
  orders: list[Order]
  blockHeight: str

reply_adapter = pydantic.TypeAdapter(Reply)
notification_adapter = pydantic.TypeAdapter(Notification)

@dataclass
class ParentSubaccounts(StreamsMixin):
  async def raw_parent_subaccounts(
    self, *, id: str, batched: bool = True, validate: bool | None = None,
  ) -> Stream[Notification, Reply, Unsubscribed]:
    """
    Subscribe to the indexer parent subaccounts feed for an address and parent subaccount number.

    - `id`: Subaccount id formatted as {address}/{subaccount-number}.
    - `batched`: Reduce incoming messages by batching contents.
    - `validate`: Whether to validate reply and update payloads against the generated schemas.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/websockets#parent-subaccounts)
    """
    stream = await self.client.subscribe(f'v4_parent_subaccounts:{id}', {'batched': batched})

    async def parsed_stream() -> AsyncIterable[Notification]:
      async for msg in stream:
        data = msg['contents']
        msgs: list[Notification] = data if batched else [data]
        for d in msgs:
          yield notification_adapter.validate_python(d) if self.validate(validate) else d

    c = stream.reply['contents']
    reply: Reply = reply_adapter.validate_python(c) if self.validate(validate) else c
    return Stream(reply, parsed_stream(), stream.unsubscribe)

