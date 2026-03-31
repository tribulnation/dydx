# Place & Manage Orders

Use `DYDX` by default for trading actions. Reach for `PrivateNode` directly only if you specifically want the lower-level node wrapper.

## Connect For Trading

`DYDX.new()` uses `DYDX_MNEMONIC` if you do not pass a mnemonic explicitly. For testnet trading with `PrivateNode.testnet()`, the default is `DYDX_TESTNET_MNEMONIC`.

```python
from dydx import DYDX

dydx = DYDX.new()
```

## Place An Order

```python
from decimal import Decimal
from dydx import DYDX

async with DYDX.new() as dydx:
  market = await dydx.indexer.data.get_market('BTC-USD')
  response = await dydx.node.place_order(
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

## Cancel An Order

```python
from decimal import Decimal
from dydx import DYDX

async with DYDX.new() as dydx:
  market = await dydx.indexer.data.get_market('BTC-USD')
  placed = await dydx.node.place_order(
  market,
  {
    'side': 'BUY',
    'size': Decimal('0.001'),
    'price': Decimal('50000'),
    'flags': 'LONG_TERM',
    'time_in_force': 'POST_ONLY',
  },
  )

async with DYDX.new() as dydx:
  response = await dydx.node.cancel_order(placed['order'].order_id)
  print(response.tx_response.code)
```

## Cancel Multiple Orders

```python
from decimal import Decimal
from dydx import DYDX

async with DYDX.new() as dydx:
  market = await dydx.indexer.data.get_market('BTC-USD')
  first = await dydx.node.place_order(
  market,
  {
    'side': 'SELL',
    'size': Decimal('0.001'),
    'price': Decimal('200000'),
    'flags': 'SHORT_TERM',
  },
  )
  second = await dydx.node.place_order(
  market,
  {
    'side': 'SELL',
    'size': Decimal('0.001'),
    'price': Decimal('200000'),
    'flags': 'SHORT_TERM',
  },
  )

  response = await dydx.node.batch_cancel_orders([first['order'].order_id, second['order'].order_id])
  print(response.tx_response.code)
```
