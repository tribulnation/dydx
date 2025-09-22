from dataclasses import dataclass

from .get_candles import GetCandles
from .get_historical_funding import GetHistoricalFunding
from .get_order import GetOrder
from .get_order_book import GetOrderBook
from .get_subaccounts import GetSubaccounts
from .list_orders import ListOrders


@dataclass
class MarketData(
  GetCandles,
  GetHistoricalFunding,
  GetOrder,
  GetOrderBook,
  GetSubaccounts,
  ListOrders,
):
  ...