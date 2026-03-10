# Authenticated Requests

Trading is handled by `PrivateNode`.

```python
from decimal import Decimal
from dydx import Indexer, PrivateNode

async with Indexer.new() as indexer:
  market = await indexer.data.get_market('BTC-USD')

node = await PrivateNode.connect()  # uses DYDX_MNEMONIC if omitted
response = await node.place_order(
  market,
  {
    'side': 'BUY',
    'size': Decimal('0.001'),
    'price': Decimal('50000'),
    'flags': 'LONG_TERM',
    'time_in_force': 'POST_ONLY',
  },
)

print(response['tx'].tx_response.code)
```

Notes:

- `market` must be a `PerpetualMarket` object, so it is natural to fetch it from `Indexer.data`
- `PrivateNode` currently uses mnemonic-based access
- this example sends a real transaction pattern, so treat it carefully
