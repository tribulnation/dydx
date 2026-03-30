# Async Usage

dYdX uses two async lifecycle patterns in this package:

- `DYDX.new()` as the default authenticated context that gives you both indexer and node access
- `Indexer.new()` for the indexer wrapper, which supports plain construction and `async with`
- `PublicNode.public()` / `PrivateNode.new()` for node-backed clients

## `DYDX`

For authenticated usage, prefer `DYDX`.

```python
from dydx import DYDX

async with DYDX.new() as dydx:
  market = await dydx.indexer.data.get_market('BTC-USD')
  price = await dydx.node.get_price(int(market['clobPairId']))
```

## Indexer

`Indexer` owns both an HTTP client and a WebSocket streams client.

For quick request-response flows, plain construction is fine because the internal HTTP and WebSocket clients open lazily on first use.

```python
from dydx import Indexer

indexer = Indexer.new()
market = await indexer.data.get_market('BTC-USD')
print(market['oraclePrice'])
```

Use `async with` when you want explicit lifecycle management, especially if you are also opening streams.

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  market = await indexer.data.get_market('BTC-USD')
```

## Streams

For streams, prefer `async with` almost always.

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  stream = await indexer.streams.block_height()
  print(stream.reply['height'])
  async for update in stream:
    print(update['blockHeight'])
    break
```

## Node Clients

`PublicNode` and `PrivateNode` use direct factory methods instead of async connection setup.

```python
from dydx.node import PublicNode, PrivateNode

public_node = PublicNode.public()
private_node = PrivateNode.new()
```

Use:

- `PublicNode.public()` for public node reads
- `PrivateNode.new()` for mnemonic-backed trading actions

## Guidance

Use `DYDX.new()` by default for authenticated/private workflows.

Use `async with Indexer.new()` by default for public/read-only ones.

Reach for plain `Indexer.new()` only for quick one-off reads.

Use `PublicNode.public()` / `PrivateNode.new()` for node clients.
