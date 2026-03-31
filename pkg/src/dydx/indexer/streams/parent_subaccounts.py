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
    """
    Subscribe to the indexer parent subaccounts feed for an address and parent subaccount number.

    - `address`: Wallet address that owns the parent subaccount.
    - `subaccount`: Parent subaccount number.
    - `batched`: Reduce incoming messages by batching contents.
    - `validate`: Whether to validate reply and update payloads against the generated schemas.

    > [Official API docs](https://docs.dydx.xyz/indexer-client/websockets#parent-subaccounts)
    """
    return await self.raw_parent_subaccounts(
      id=f'{address}/{subaccount}',
      batched=batched,
      validate=validate,
    )
