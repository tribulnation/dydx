# Typed dYdX

> A fully typed, validated async client for the dYdX Indexer, Node and CosmosSDK/CometBFT APIs.

```python
from dydx import Dydx

async with Dydx.testnet(public=True) as client:
  market = await client.indexer.data.get_market('BTC-USD')
  stream = await client.indexer.streams.markets()
  balances = await client.chain.bank.all_balances('dydx1...')
  block = await client.chain.comet.block()
  clob_pairs = await client.node.public.get_clob_pairs()

  print(market['oraclePrice'])
  print(stream.reply['markets']['BTC-USD']['oraclePrice'])
  print(balances)
  print(block['block']['header']['height'])
  print(clob_pairs)
  await stream.unsubscribe()
```

## Package Shape

- `client.indexer.data`: indexer HTTP reads for markets, orders, fills, transfers, and account history
- `client.indexer.streams`: indexer WebSocket subscriptions
- `client.chain`: Cosmos gRPC module queries for balances, CLOB metadata, prices, subaccounts, staking, and transactions
- `client.chain.comet`: CometBFT HTTP RPC reads for blocks, transaction lookup, and transaction search
- `client.node`: wallet-aware signing, order placement, cancellation, and transaction helpers

## Installation

```bash
pip install typed-dydx
```

## Documentation

- [Wallet Setup](https://dydx.tribulnation.com/api-keys/)
- [How To](https://dydx.tribulnation.com/how-to/)
- [Reference](https://dydx.tribulnation.com/reference/)

## Source Code

> [github.com/tribulnation/dydx](https://github.com/tribulnation/dydx)
