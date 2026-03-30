# Fetch Transactions

Use `Indexer.data` for historical account activity.

```python
import os

address = 'dydx1...'
address = os.environ['DYDX_ADDRESS']
subaccount = 0
market = 'BTC-USD'
```

## Fetch Fills

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  fills = await indexer.data.get_fills(
    address,
    subaccount=subaccount,
    market=market,
    market_type='PERPETUAL',
    limit=100,
  )
  print(fills['fills'][0]['price'])
```

For longer backfills, use `get_fills_paged(...)`.

## Fetch Funding Payments

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  funding = await indexer.data.get_funding_payments(
    address,
    subaccount=subaccount,
    ticker=market,
    limit=100,
  )
  print(funding['fundingPayments'][0]['payment'])
```

For longer backfills, use `get_funding_payments_paged(...)`.

## Fetch Transfers

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  transfers = await indexer.data.get_transfers(
    address,
    subaccount=subaccount,
    limit=100,
  )
  print(transfers['transfers'][0]['size'])
```

For longer backfills, use `get_transfers_paged(...)`.
