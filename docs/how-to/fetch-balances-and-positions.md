# Fetch Balances & Positions

Use `Indexer.data` for account-state reads.

```python
import os

address = 'dydx1...'
address = os.environ['DYDX_ADDRESS']
subaccount = 0
```

## Fetch A Subaccount

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  account = await indexer.data.get_subaccount(address, subaccount)
  print(account['subaccount']['equity'])
```

## Fetch All Subaccounts

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  accounts = await indexer.data.get_subaccounts(address)
  print(len(accounts['subaccounts']))
```

## Fetch Positions

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  positions = await indexer.data.list_positions(
    address,
    subaccount=subaccount,
  )
  print(len(positions['positions']))
```

If you want a single open position, use `get_open_position(address, market, subaccount=...)`.

## Fetch Asset Positions

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  asset_positions = await indexer.data.get_asset_positions(
    address,
    subaccount=subaccount,
    validate=False,
  )
  print(asset_positions['positions'])
```
