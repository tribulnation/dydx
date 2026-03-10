# Public Data

Use `Indexer` for market metadata and order books, and `PublicNode` when you need public node reads.

```python
from dydx import Indexer, PublicNode

async with Indexer.new() as indexer:
  market = await indexer.data.get_market('BTC-USD')
  book = await indexer.data.get_order_book('BTC-USD')

public_node = await PublicNode.connect()
price = await public_node.get_price(int(market['clobPairId']))

print(market['oraclePrice'])
print(book['bids'][0])
print(price)
```

This split is useful because the indexer is the best entry point for most application reads, while the public node wrapper exposes a few direct node-level queries.
