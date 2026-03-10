# Environment Variables

## Public Usage

No environment variables are required for:

- `Indexer`
- `PublicNode`

## Private Trading Usage

The only environment variable currently used by the library itself is:

```bash
DYDX_MNEMONIC=
```

`PrivateNode.connect()` reads `DYDX_MNEMONIC` if you do not pass a mnemonic explicitly.

## URLs And Endpoints

Custom URLs are configured through function arguments, not environment variables:

```python
from dydx import Indexer, PublicNode, PrivateNode

indexer = Indexer.new(
  http_url='https://indexer.dydx.trade/',
  ws_url='wss://indexer.dydx.trade/v4/ws',
)

public_node = await PublicNode.connect(url='oegs.dydx.trade:443')
private_node = await PrivateNode.connect(url='oegs.dydx.trade:443')
```
