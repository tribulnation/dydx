# API Overview

The package exposes three public entry points:

- `Indexer`
- `PublicNode`
- `PrivateNode`

That split mirrors the official dYdX documentation, which separates the indexer APIs from the node APIs.

## Indexer

Use `Indexer` for most data retrieval.

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  ...
```

### `Indexer.data`

Implemented read methods include:

- `get_markets`, `get_market`
- `get_order_book`
- `get_trades`
- `get_candles`, `get_candles_paged`
- `get_fills`, `get_fills_paged`
- `get_funding_payments`, `get_funding_payments_paged`
- `get_historical_funding`, `get_historical_funding_paged`
- `get_subaccount`, `get_subaccounts`
- `get_transfers`, `get_transfers_paged`
- `list_orders`
- `list_positions`

### `Indexer.streams`

Current stream coverage:

- `subaccounts(address, subaccount=0, batched=True)`

## PublicNode

Use `PublicNode` for public node reads backed by the dYdX node client.

```python
from dydx import PublicNode

node = await PublicNode.connect()
```

Implemented methods:

- `get_clob_pair(id)`
- `get_price(id)`
- `get_user_fee_tier(address)`

## PrivateNode

Use `PrivateNode` for signed trading actions.

```python
from dydx import PrivateNode

node = await PrivateNode.connect()
```

Implemented methods:

- `place_order(market, order, ...)`
- `cancel_order(order_id, ...)`
- `batch_cancel_orders(order_ids, ...)`

## Credentials

- `Indexer` requires no credentials
- `PublicNode` requires no credentials
- `PrivateNode` currently supports mnemonic-based access

See [Trading Access](api-keys.md) for the current authentication model.
