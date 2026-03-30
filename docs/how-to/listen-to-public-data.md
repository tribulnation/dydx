# Listen To Public Data

Use `Indexer.streams` for public subscription-style updates.

## Listen To Trades

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  stream = await indexer.streams.trades(id='BTC-USD')
  print(stream.reply['trades'][0]['price'])
```

## Listen To Candles

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  stream = await indexer.streams.candles('BTC-USD', resolution='1MIN')
  print(stream.reply['candles'][0]['close'])
  async for update in stream:
    print(update['close'])
    break
```

## Listen To Markets

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  stream = await indexer.streams.markets()
  print(stream.reply['markets']['BTC-USD']['oraclePrice'])
  async for update in stream:
    print(update)
    break
```

## Listen To Block Height

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  stream = await indexer.streams.block_height()
  print(stream.reply['height'])
  async for update in stream:
    print(update['blockHeight'])
    break
```
