# Streams

The current stream wrapper focuses on indexer subaccount updates.

```python
from dydx import Indexer

async with Indexer.new() as indexer:
  initial, updates = await indexer.streams.subaccounts('dydx...', subaccount=0)

  print(initial['subaccount']['equity'])

  async for update in updates:
    if fills := update.get('fills'):
      print(fills)
```

This stream can include updates for:

- positions
- orders
- fills
- transfers
- trading rewards
