from typing_extensions import NotRequired, AsyncIterable
from dataclasses import dataclass

from dydx.core import TypedDict, validator
from dydx.core.types import (
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
  createdAt: str
  createdAtHeight: str
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
  ticker: str
  price: str
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
  createdAtHeight: str
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
  createdAt: str
  createdAtHeight: str

class TradingReward(TypedDict):
  """https://docs.dydx.xyz/types/trading_reward_subaccount_message"""
  tradingReward: str
  createdAt: str
  createdAtHeight: str

class UpdateMessage(TypedDict):
  perpetualPositions: NotRequired[list[UpdatePerpetualPosition]]
  assetPositions: NotRequired[list[UpdateAssetPosition]]
  orders: NotRequired[list[UpdateOrder]]
  fills: NotRequired[list[Fill]]
  transfers: NotRequired[list[Transfer]]
  tradingRewards: NotRequired[list[TradingReward]]
  blockHeight: NotRequired[str|None]

validate_update = validator(UpdateMessage)
validate_update_batch = validator(list[UpdateMessage])

@dataclass
class Subaccounts(StreamsMixin):
  async def subaccounts(
    self, address: str, *, subaccount: int,
    validate: bool | None = None, batched: bool = True,
  ) -> tuple[InitialSubaccount, AsyncIterable[UpdateMessage]]:
    res, stream = await self.client.subscribe('v4_subaccounts', id=f'{address}/{subaccount}', batched=batched)

    async def gen():
      async for msg in stream:
        data = msg['contents']
        msgs: list = data if batched else [data]
        for d in msgs:
          yield validate_update(d) if self.validate(validate) else d

    data = res['contents']
    if self.validate(validate):
      data = validate_initial_message(data)
    
    return data, gen()
