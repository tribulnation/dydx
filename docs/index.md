# Typed dYdX

> A fully typed, validated async client for the dYdX v4 APIs.

**Use autocomplete instead of documentation.**

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  btc = await indexer.data.get_market('BTC-USD')
  print(btc['oraclePrice'])
```

## Why Typed dYdX?

- **🎯 Precise Types**: Literal types where they help, so your IDE knows what is valid.
- **✅ Automatic Validation**: Catch upstream API changes earlier.
- **⚡ Async First**: Built for concurrent, network-heavy workflows.
- **🔒 Type Safety**: Full type hints throughout.
- **🎨 Better DX**: Clear routing, sensible defaults, optional complexity.
- **📦 Batteries Included**: Pagination, streams, and helpers when they earn their place.

## Installation

```bash
pip install typed-dydx
```

## Quick Start

The package exposes three entry points because dYdX itself is split across the indexer and node APIs:

- `Indexer` from `dydx` for HTTP market/account data and WebSocket streams
- `PublicNode` from `dydx.node` for public node reads
- `PrivateNode` from `dydx.node` for signed trading actions

```python
from dydx import Indexer
from dydx.node import PublicNode

async with Indexer.new() as indexer:
  market = await indexer.data.get_market('BTC-USD')

public_node = PublicNode.public()
price = await public_node.get_price(int(market['clobPairId']))
```

## Features

### No Unnecessary Imports

Notice something? **You never imported `Literal` types.** Just use strings:

```python
# ❌ Other libraries
# trades = await client.get_trades(Market.BTC_USD)

# ✅ Typed dYdX
async with Indexer.new() as indexer:
  trades = await indexer.data.get_trades('BTC-USD', limit=50)
```

### Precise Type Annotations

Every field is precisely typed. Market metadata is strongly shaped enough to use directly:

```python
from decimal import Decimal

async with Indexer.new() as indexer:
  btc = await indexer.data.get_market('BTC-USD')

clob_pair_id: str = btc['clobPairId']
oracle_price: Decimal = btc['oraclePrice']
```

### Automatic Validation

Response validation is **on by default** but can be disabled:

```python
# Validated (default) - throws ValidationError if API response changes
async with Indexer.new() as indexer:
  markets = await indexer.data.get_markets(limit=5)

# Skip validation for maximum performance
async with Indexer.new(validate=False) as indexer:
  markets = await indexer.data.get_markets(limit=5)
```

### Built-in Pagination

```python
import os

async with Indexer.new() as indexer:
  async for chunk in indexer.data.get_fills_paged(
    os.environ['DYDX_ADDRESS'],
    subaccount=0,
    market='BTC-USD',
    market_type='PERPETUAL',
    limit=100,
  ):
    print(len(chunk))
```

### WebSocket Streams

Real-time user data comes from the indexer WebSocket API:

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  stream = await indexer.streams.subaccounts('dydx1039f5sxkl0t39vxcsnmlu62ly22typdap0zkyn', subaccount=0)
  print(stream.reply['subaccount']['equity'])
```

## API Coverage

Current coverage is split across:

- `Indexer.data` for markets, order books, candles, trades, fills, transfers, subaccounts, funding, orders, and positions
- `Indexer.streams` for subaccount updates
- `PublicNode` for price, CLOB pair, and fee-tier reads
- `PrivateNode` for placing and cancelling orders

📋 See [API Overview](api-overview.md) for the current structure and coverage.

## Documentation

- [**Getting Started**](getting-started.md) - Install the package and make your first requests
- [**Trading Access**](api-keys.md) - Configure mnemonic-based trading access
- [**API Overview**](api-overview.md) - Understand the client structure and coverage
- [**How To**](how-to/index.md) - Task-focused guides for market data, account data, trading, and streams
- [**Reference**](reference/index.md) - Error handling, env vars, and endpoint overview

## Design Philosophy

Typed dYdX follows the principles outlined in [this blog post](https://tribulnation.com/blog/clients).

*Details matter. Developer experience matters.*
