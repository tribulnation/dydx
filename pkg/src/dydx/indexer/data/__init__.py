from dataclasses import dataclass

from .core import INDEXER_HTTP_URL, INDEXER_TESTNET_HTTP_URL
from .api.get_asset_positions import GetAssetPositions
from .get_candles_paged import GetCandlesPaged
from .api.get_compliance_screen import GetComplianceScreen
from .get_fills_paged import GetFillsPaged
from .get_funding_payments_paged import GetFundingPaymentsPaged
from .api.get_funding_payments_for_parent_subaccount import GetFundingPaymentsForParentSubaccount
from .api.get_height import GetHeight
from .get_historical_funding_paged import GetHistoricalFundingPaged
from .api.get_historical_pnl import GetHistoricalPnl
from .get_market import GetMarket
from .api.get_megavault_historical_pnl import GetMegavaultHistoricalPnl
from .api.get_order import GetOrder
from .api.get_order_book import GetOrderBook
from .api.get_parent_asset_positions import GetParentAssetPositions
from .api.get_parent_fills import GetParentFills
from .api.get_parent_historical_pnl import GetParentHistoricalPnl
from .api.get_parent_subaccount import GetParentSubaccount
from .api.get_parent_transfers import GetParentTransfers
from .api.get_rewards import GetRewards
from .api.get_rewards_aggregated import GetRewardsAggregated
from .api.get_screen import GetScreen
from .api.get_sparklines import GetSparklines
from .api.get_subaccount import GetSubaccount
from .api.get_subaccounts import GetSubaccounts
from .api.get_time import GetTime
from .api.get_trades import GetTrades
from .get_transfers_paged import GetTransfersPaged
from .api.get_transfers_between import GetTransfersBetween
from .api.get_vaults_historical_pnl import GetVaultsHistoricalPnl
from .api.list_orders import ListOrders
from .api.list_parent_orders import ListParentOrders
from .api.list_parent_positions import ListParentPositions
from .get_open_position import GetOpenPosition

@dataclass
class IndexerData(
  GetAssetPositions,
  GetCandlesPaged,
  GetComplianceScreen,
  GetFillsPaged,
  GetFundingPaymentsPaged,
  GetFundingPaymentsForParentSubaccount,
  GetHeight,
  GetHistoricalFundingPaged,
  GetHistoricalPnl,
  GetMarket,
  GetMegavaultHistoricalPnl,
  GetOrder,
  GetOrderBook,
  GetParentAssetPositions,
  GetParentFills,
  GetParentHistoricalPnl,
  GetParentSubaccount,
  GetParentTransfers,
  GetRewards,
  GetRewardsAggregated,
  GetScreen,
  GetSparklines,
  GetSubaccount,
  GetSubaccounts,
  GetTime,
  GetTrades,
  GetTransfersPaged,
  GetTransfersBetween,
  GetVaultsHistoricalPnl,
  ListOrders,
  ListParentOrders,
  ListParentPositions,
  GetOpenPosition,
):
  ...
