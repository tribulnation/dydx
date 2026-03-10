from dataclasses import dataclass as _dataclass

from .get_clob_pair import GetClobPair
from .get_price import GetPrice
from .get_user_fee_tier import GetUserFeeTier

@_dataclass
class PublicNode(GetClobPair, GetPrice, GetUserFeeTier):
  ...