from dataclasses import dataclass

from .api.subaccounts import Subaccounts as SubaccountsAPI, Notification

@dataclass
class Subaccounts(SubaccountsAPI):
  async def subaccounts(
    self, address: str, *,
    subaccount: int,
    validate: bool | None = None,
    batched: bool = True,
  ):
    """Subscribe to subaccount updates using address and subaccount number."""
    return await self.raw_subaccounts(
      id=f'{address}/{subaccount}',
      batched=batched,
      validate=validate,
    )
