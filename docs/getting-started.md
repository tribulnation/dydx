# Getting Started

This guide gets you from installation to your first indexer and node requests.

## Install The Package

```bash
pip install typed-dydx
```

## Use The Indexer For Market Data

Start with the indexer. It covers most read-heavy workflows and also owns the WebSocket streams wrapper.

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  markets = await indexer.data.get_markets(limit=5)
  btc = await indexer.data.get_market('BTC-USD')
  book = await indexer.data.get_order_book('BTC-USD')

print(markets['markets']['BTC-USD']['oraclePrice'])
print(btc['oraclePrice'])
print(book['bids'][0])
```

## Use The Public Node For Node Reads

The public node wrapper is separate from the indexer wrapper:

```python
from dydx import Indexer
from dydx.node import PublicNode

async with Indexer.new() as indexer:
  market = await indexer.data.get_market('BTC-USD')

node = PublicNode.public()
price = await node.get_price(int(market['clobPairId']))
```

## Use The Private Node For Trading

Trading goes through `PrivateNode`. This wrapper currently uses mnemonic-based access.

```python
from decimal import Decimal
from dydx import Indexer
from dydx.node import PrivateNode

async with Indexer.new() as indexer:
  market = await indexer.data.get_market('BTC-USD')

node = PrivateNode.new()  # uses DYDX_MNEMONIC if omitted
result = await node.place_order(
  market,
  {
    'side': 'BUY',
    'size': Decimal('0.001'),
    'price': Decimal('50000'),
    'flags': 'LONG_TERM',
    'time_in_force': 'POST_ONLY',
  },
)
```

`PrivateNode` currently supports mnemonic-based access only.

## Context Manager Pattern

Use `async with` for `Indexer`, since it owns HTTP and WebSocket clients:

```python
async with Indexer.new() as indexer:
  ...
```

`PublicNode` and `PrivateNode` use direct factories: `PublicNode.public()` and `PrivateNode.new()`.

## Next Steps

- Read [Trading Access](api-keys.md) before using `PrivateNode`
- Read [API Overview](api-overview.md) to understand the split between indexer and node clients
- Browse [How To](how-to/index.md) for practical workflows
