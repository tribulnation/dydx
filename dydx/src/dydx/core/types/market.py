from typing_extensions import Literal
from dydx.core import TypedDict

MarketType = Literal['CROSS', 'ISOLATED']
MarketStatus = Literal['ACTIVE', 'PAUSED', 'CANCEL_ONLY', 'POST_ONLY', 'INITIALIZING', 'FINAL_SETTLEMENT']

class PerpetualMarket(TypedDict):
  """Perpetual Market Object

  > [dYdX API docs](https://docs.dydx.xyz/types/perpetual_market)
  """
  clobPairId: str
  ticker: str
  status: MarketStatus
  oraclePrice: str
  priceChange24H: str
  volume24H: str
  trades24H: int
  nextFundingRate: str
  initialMarginFraction: str
  maintenanceMarginFraction: str
  openInterest: str
  atomicResolution: int
  quantumConversionExponent: int
  tickSize: str
  stepSize: str
  stepBaseQuantums: int
  subticksPerTick: int
  marketType: MarketType
  openInterestLowerCap: str
  openInterestUpperCap: str
  baseOpenInterest: str
  defaultFundingRate1H: str