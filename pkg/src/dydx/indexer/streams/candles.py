from typing_extensions import Literal
from dataclasses import dataclass

from .api.candles import Candles as CandlesAPI

Resolution = Literal['1MIN', '5MINS', '15MINS', '30MINS', '1HOUR', '4HOURS', '1DAY']


@dataclass
class Candles(CandlesAPI):
  async def candles(
    self,
    market: str,
    *,
    resolution: Resolution,
    validate: bool | None = None,
    batched: bool = True,
  ):
    """Subscribe to candle updates using market and resolution."""
    return await self.raw_candles(
      id=f'{market}/{resolution}',
      batched=batched,
      validate=validate,
    )
