# Paginate Through Results

dYdX indexer endpoints use page-number pagination for several account-history
resources. The client exposes both one-shot methods and paged helpers where the
package has a typed pagination wrapper.

```python
from dydx import Dydx

async with Dydx.testnet(public=True) as client:
  first_page = await client.indexer.data.get_fills(
    'dydx1...',
    subaccount=0,
  )
  print(first_page)
```

```python
from dydx import Dydx

async with Dydx.testnet(public=True) as client:
  pages = client.indexer.data.get_fills_paged(
    'dydx1...',
    subaccount=0,
    limit=100,
  )
  async for page in pages:
    for fill in page:
      print(fill)
```

Paged helpers are currently available for fills, transfers, funding payments,
historical funding, and candles. Use timestamp or height filters when doing
backfills so repeated runs have a stable upper bound.
