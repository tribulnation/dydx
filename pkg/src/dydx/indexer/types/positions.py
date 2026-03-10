from typing_extensions import NotRequired, Literal
from decimal import Decimal

from dydx.core import TypedDict
from .enums import PositionSide

PerpetualPositionStatus = Literal['OPEN', 'CLOSED', 'LIQUIDATED']
"""Perpetual Position Status

> [dYdX API docs](https://docs.dydx.xyz/types/perpetual_position_status)
"""

class PerpetualPosition(TypedDict):
  """Perpetual Position Response Object

  > [dYdX API docs](https://docs.dydx.xyz/types/perpetual_position_response_object)
  """
  market: str
  status: PerpetualPositionStatus
  side: PositionSide
  size: Decimal
  maxSize: Decimal
  entryPrice: Decimal
  exitPrice: NotRequired[Decimal|None]
  realizedPnl: NotRequired[Decimal|None]
  unrealizedPnl: NotRequired[Decimal|None]
  createdAt: str
  createdAtHeight: str
  closedAt: NotRequired[str|None]
  sumOpen: Decimal
  sumClose: Decimal
  netFunding: Decimal
  subaccountNumber: int

class AssetPosition(TypedDict):
  """Asset Position Response Object

  > [dYdX API docs](https://docs.dydx.xyz/types/asset_position_response_object)
  """
  size: str
  symbol: str
  side: PositionSide
  assetId: str
  subaccountNumber: int