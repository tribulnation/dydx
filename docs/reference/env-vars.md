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

`DYDX.new()` and `PrivateNode.new()` read `DYDX_MNEMONIC` if you do not pass a mnemonic explicitly.

## URLs And Endpoints

Custom URLs are configured through function arguments, not environment variables:

```python
from dydx import DYDX, Indexer
from dydx.node import PublicNode, PrivateNode

indexer = Indexer.new(
  http_url='https://indexer.dydx.trade/',
  ws_url='wss://indexer.dydx.trade/v4/ws',
)

dydx = DYDX.new(
  node_url='oegs.dydx.trade:443',
  rest_indexer='https://indexer.dydx.trade/',
  websocket_indexer='wss://indexer.dydx.trade/v4/ws',
)

public_node = PublicNode.public(url='oegs.dydx.trade:443')
private_node = PrivateNode.new(url='oegs.dydx.trade:443')
```
