# API Overview

The package exposes three public entry points:

- `DYDX`
- `Indexer`
- `PublicNode`
- `PrivateNode`

That split mirrors the official dYdX documentation, which separates the indexer APIs from the node APIs.

## `DYDX`

Use `DYDX` by default when you need authenticated/private usage. It combines the indexer and node clients behind one context manager.

```python
from dydx import DYDX

async with DYDX.new() as dydx:
  ...
```

`DYDX.indexer` exposes the full `Indexer` surface, and `DYDX.node` exposes the combined node surface.

## Indexer

Use `Indexer` for public/read-only data retrieval when you do not need trading access.

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  ...
```

### `Indexer.data`

Implemented HTTP read methods include:

- `get_asset_positions`
- `get_candles`, `get_candles_paged`
- `get_compliance_screen`
- `get_fills`, `get_fills_paged`
- `get_funding_payments`, `get_funding_payments_paged`
- `get_funding_payments_for_parent_subaccount`
- `get_height`
- `get_historical_funding`, `get_historical_funding_paged`
- `get_historical_pnl`
- `get_markets`, `get_market`
- `get_megavault_historical_pnl`, `get_megavault_positions`
- `get_order`, `get_order_book`
- `get_parent_asset_positions`
- `get_parent_fills`
- `get_parent_historical_pnl`
- `get_parent_subaccount`
- `get_parent_subaccount_fills`
- `get_parent_subaccount_orders`
- `get_parent_subaccount_transfers`
- `get_parent_transfers`
- `get_rewards`, `get_rewards_aggregated`
- `get_screen`, `get_sparklines`
- `get_subaccount`, `get_subaccounts`
- `get_time`, `get_trades`
- `get_transfers`, `get_transfers_paged`, `get_transfers_between`
- `get_vaults_historical_pnl`
- `list_orders`, `list_parent_orders`
- `list_parent_positions`, `list_positions`, `get_open_position`

`Indexer.data` includes the full documented read surface, along with convenience methods such as `get_market()`, `get_open_position()`, and the `*_paged()` iterators.

### `Indexer.streams`

Current stream coverage:

- `block_height(batched=True)`
- `candles(market, resolution=..., batched=True)`
- `markets(batched=True)`
- `orders(id=..., batched=True)`
- `parent_subaccounts(address, subaccount=0, batched=True)`
- `subaccounts(address, subaccount=0, batched=True)`
- `trades(id=..., batched=True)`

## PublicNode

Use `PublicNode` for public node reads backed by the dYdX node client.

```python
from dydx.node import PublicNode

node = PublicNode.public()
```

Implemented methods:

- `get_clob_pair(id)`
- `get_price(id)`
- `get_user_fee_tier(address)`

## PrivateNode

Use `PrivateNode` directly only when you specifically want the lower-level node wrapper. Prefer `DYDX` for most authenticated workflows.

```python
from dydx.node import PrivateNode

node = PrivateNode.new()
```

Implemented methods:

- `place_order(market, order, ...)`
- `cancel_order(order_id, ...)`
- `batch_cancel_orders(order_ids, ...)`

## Credentials

- `Indexer` requires no credentials
- `PublicNode` requires no credentials
- `DYDX` currently supports mnemonic-based access for `node`
- `PrivateNode` currently supports mnemonic-based access

See [Trading Access](api-keys.md) for the current authentication model.
