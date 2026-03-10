from typing_extensions import NotRequired, AsyncIterable, cast
from dataclasses import dataclass

from dydx.core import TypedDict, validator
from dydx.indexer.types import (
  PositionSide, Liquidity, FillType,
  OrderState, OrderSide, OrderType, TimeInForce, OrderStatus,
  PerpetualPosition, AssetPosition,
  Account, TransferType,
)
from .core import StreamsMixin

class InitialSubaccount(TypedDict):
  assetPositions: dict[str, AssetPosition]
  address: str
  subaccountNumber: int
  equity: str
  freeCollateral: str
  latestProcessedBlockHeight: str
  marginEnabled: bool
  openPerpetualPositions: dict[str, PerpetualPosition]
  updatedAtHeight: str

class InitialMessage(TypedDict):
  subaccount: InitialSubaccount
  orders: list[OrderState]
  blockHeight: str

validate_initial_message = validator(InitialMessage)

class UpdatePerpetualPosition(TypedDict):
  """https://docs.dydx.xyz/types/perpetual_position_subaccount_message"""
  market: str
  status: str
  side: PositionSide
  size: str
  maxSize: str
  entryPrice: str
  exitPrice: NotRequired[str|None]
  realizedPnl: NotRequired[str|None]
  unrealizedPnl: NotRequired[str|None]
  createdAt: NotRequired[str|None]
  createdAtHeight: NotRequired[str|None]
  closedAt: NotRequired[str|None]
  sumOpen: str
  sumClose: str
  netFunding: str
  subaccountNumber: int

class UpdateAssetPosition(TypedDict):
  """https://docs.dydx.xyz/types/asset_position_subaccount_message"""
  address: str
  subaccountNumber: int
  positionId: str
  assetId: str
  symbol: str
  side: PositionSide
  size: str

class UpdateOrder(TypedDict):
  """https://docs.dydx.xyz/types/order_subaccount_message"""
  id: str
  subaccountId: str
  clientId: str
  clobPairId: str
  side: OrderSide
  size: str
  ticker: NotRequired[str|None]
  price: NotRequired[str|None]
  type: OrderType
  timeInForce: TimeInForce
  postOnly: NotRequired[bool|None]
  reduceOnly: NotRequired[bool|None]
  status: OrderStatus
  orderFlags: NotRequired[str|None]
  totalFilled: NotRequired[str|None]
  totalOptimisticFilled: NotRequired[str|None]
  goodTilBlock: NotRequired[str|None]
  goodTilBlockTime: NotRequired[str|None]
  triggerPrice: NotRequired[str|None]
  updatedAt: NotRequired[str|None]
  updatedAtHeight: NotRequired[str|None]
  removalReason: NotRequired[str|None]
  createdAtHeight: NotRequired[str|None]
  clientMetadata: NotRequired[str|None]

class Fill(TypedDict):
  """https://docs.dydx.xyz/types/fill_subaccount_message"""
  id: str
  subaccountId: str
  side: OrderSide
  liquidity: Liquidity
  type: FillType
  clobPairId: str
  size: str
  price: str
  quoteAmount: str
  eventId: str
  transactionHash: str
  createdAt: str
  createdAtHeight: NotRequired[str|None]
  ticker: str
  orderId: NotRequired[str|None]
  clientMetadata: NotRequired[str|None]

class Transfer(TypedDict):
  """https://docs.dydx.xyz/types/transfer_subaccount_message"""
  sender: Account
  recipient: Account
  symbol: str
  size: str
  type: TransferType
  transactionHash: str
  createdAt: NotRequired[str|None]
  createdAtHeight: NotRequired[str|None]

class TradingReward(TypedDict):
  """https://docs.dydx.xyz/types/trading_reward_subaccount_message"""
  tradingReward: str
  createdAt: NotRequired[str|None]
  createdAtHeight: NotRequired[str|None]

class UpdateMessage(TypedDict):
  """https://docs.dydx.xyz/types/subaccounts_update_message"""
  perpetualPositions: NotRequired[list[UpdatePerpetualPosition]]
  assetPositions: NotRequired[list[UpdateAssetPosition]]
  orders: NotRequired[list[UpdateOrder]]
  fills: NotRequired[list[Fill]]
  transfers: NotRequired[list[Transfer] | Transfer] # API says its a list, but in practice it seems it's always a single object
  tradingRewards: NotRequired[list[TradingReward]]
  blockHeight: NotRequired[str|None]

validate_update = validator(UpdateMessage)
validate_update_batch = validator(list[UpdateMessage])

@dataclass
class Subaccounts(StreamsMixin):
  async def subaccounts(
    self, address: str, *, subaccount: int,
    validate: bool | None = None, batched: bool = True,
  ) -> tuple[InitialMessage, AsyncIterable[UpdateMessage]]:
    res, stream = await self.client.subscribe('v4_subaccounts', id=f'{address}/{subaccount}', batched=batched)

    async def gen():
      async for msg in stream:
        data = msg['contents']
        msgs: list[UpdateMessage] = data if batched else [data]
        for d in msgs:
          try:
            validate_update(d)
          except Exception as e:
            import traceback
            import sys
            print('Validation error:', traceback.format_exc(), file=sys.stderr)
          yield validate_update(d) if self.validate(validate) else cast(UpdateMessage, d)

    c = res['contents']
    data = validate_initial_message(c) if self.validate(validate) else cast(InitialMessage, c)
    return data, gen()
