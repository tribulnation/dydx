from dataclasses import dataclass as _dataclass

from .batch_cancel_orders import BatchCancelOrders
from .cancel_order import CancelOrder
from .place_order import PlaceOrder

@_dataclass
class PrivateNode(BatchCancelOrders, CancelOrder, PlaceOrder):
  ...