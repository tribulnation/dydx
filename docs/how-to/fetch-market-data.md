# Fetch Market Data

Use `Indexer.data` for most market reads and `PublicNode` for the node-level reads this package exposes.

## Fetch Markets

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  markets = await indexer.data.get_markets(limit=5)
  btc = await indexer.data.get_market('BTC-USD')
  print(markets['markets']['BTC-USD']['oraclePrice'])
  print(btc['oraclePrice'])
```

## Fetch The Order Book

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  book = await indexer.data.get_order_book('BTC-USD')
  print(book['bids'][0], book['asks'][0])
```

## Fetch Candles

```python
from datetime import datetime, timedelta
from dydx import Indexer

to_iso = datetime.now()
from_iso = to_iso - timedelta(hours=1)

async with Indexer.new() as indexer:
  candles = await indexer.data.get_candles(
    'BTC-USD',
    resolution='1MIN',
    from_iso=from_iso,
    to_iso=to_iso,
    limit=60,
  )
  print(candles['candles'][-1]['close'])
```

## Fetch Trades

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  trades = await indexer.data.get_trades('BTC-USD', limit=50)
  print(trades['trades'][0]['price'])
```

## Fetch The Current Height

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  height = await indexer.data.get_height()
  print(height['height'])
```

## Fetch Public Node Data

```python
from dydx import Indexer
from dydx.node import PublicNode

async with Indexer.new() as indexer:
  market = await indexer.data.get_market('BTC-USD')

node = PublicNode.public()
price = await node.get_price(int(market['clobPairId']))
print(price)
```
