# Listen To Account Updates

Use `Indexer.streams.subaccounts()` for subaccount-level account updates.

```python
import os
from dydx import Indexer

address = os.environ['DYDX_ADDRESS']

async with Indexer.new() as indexer:
  stream = await indexer.streams.subaccounts(address, subaccount=0)
  print(stream.reply['subaccount']['equity'])
```

This stream can include updates for:

- positions
- orders
- fills
- transfers
- trading rewards
