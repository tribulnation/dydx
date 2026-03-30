from dataclasses import dataclass

from .api.parent_subaccounts import ParentSubaccounts as ParentSubaccountsAPI

@dataclass
class ParentSubaccounts(ParentSubaccountsAPI):
  async def parent_subaccounts(
    self, address: str, *,
    subaccount: int,
    validate: bool | None = None,
    batched: bool = True,
  ):
    """Subscribe to parent subaccount updates using address and subaccount number."""
    return await self.raw_parent_subaccounts(
      id=f'{address}/{subaccount}',
      batched=batched,
      validate=validate,
    )
