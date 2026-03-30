from dataclasses import dataclass

from .api.list_positions import ListPositions, PerpetualPosition


@dataclass
class GetOpenPosition(ListPositions):
  async def get_open_position(
    self,
    address: str,
    market: str,
    *,
    subaccount: int,
    validate: bool | None = None,
  ) -> PerpetualPosition | None:
    """Retrieves the open perpetual position for a specific subaccount."""
    response = await self.list_positions(
      address,
      subaccount=subaccount,
      status='OPEN',
      validate=validate,
    )
    positions = response['positions']
    for position in positions:
      if position['market'] == market:
        return position
    return None
