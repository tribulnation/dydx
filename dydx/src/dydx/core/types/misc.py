from dydx.core import TypedDict

class Account(TypedDict):
  """Account Object

  > [dYdX API docs](https://docs.dydx.xyz/types/account)
  """
  address: str
  subaccountNumber: int