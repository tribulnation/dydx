from dataclasses import dataclass

from .get_candles import GetCandles
from .get_fills import GetFills
from .get_funding_payments import GetFundingPayments
from .get_historical_funding import GetHistoricalFunding
from .get_markets import GetMarkets
from .get_order import GetOrder
from .get_order_book import GetOrderBook
from .get_subaccounts import GetSubaccounts
from .get_trades import GetTrades
from .list_orders import ListOrders
from .list_positions import ListPositions


@dataclass
class IndexerData(
  GetCandles,
  GetFills,
  GetFundingPayments,
  GetHistoricalFunding,
  GetMarkets,
  GetOrder,
  GetOrderBook,
  GetSubaccounts,
  GetTrades,
  ListOrders,
  ListPositions,
):
  ...