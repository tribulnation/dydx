from typing_extensions import Literal, TypedDict, NotRequired
from decimal import Decimal

MarketType = Literal['CROSS', 'ISOLATED']
MarketStatus = Literal['ACTIVE', 'PAUSED', 'CANCEL_ONLY', 'POST_ONLY', 'INITIALIZING', 'FINAL_SETTLEMENT']

class PerpetualMarket(TypedDict):
  """Perpetual Market Object

  > [dYdX API docs](https://docs.dydx.xyz/types/perpetual_market)
  """
  clobPairId: str
  ticker: str
  status: MarketStatus
  oraclePrice: Decimal
  priceChange24H: Decimal
  volume24H: Decimal
  trades24H: int
  nextFundingRate: Decimal
  initialMarginFraction: Decimal
  maintenanceMarginFraction: Decimal
  openInterest: Decimal
  atomicResolution: int
  quantumConversionExponent: int
  tickSize: Decimal
  stepSize: Decimal
  stepBaseQuantums: int
  subticksPerTick: int
  marketType: MarketType
  openInterestLowerCap: NotRequired[Decimal]
  openInterestUpperCap: NotRequired[Decimal]
  baseOpenInterest: Decimal
  defaultFundingRate1H: NotRequired[Decimal]