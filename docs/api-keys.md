# Trading Access

For dYdX, the important distinction is not public vs API-key access. It is indexer vs node access.

## Public Usage

No credentials are required for:

- `Indexer`
- `PublicNode`

## Private Trading Setup

`PrivateNode` currently uses mnemonic-based access.

```bash
export DYDX_MNEMONIC="your twelve or twenty-four word mnemonic"
```

```python
from dydx import PrivateNode

node = await PrivateNode.connect(mnemonic="your mnemonic here")
```

## Security Notes

- never commit your mnemonic
- treat `DYDX_MNEMONIC` as a high-sensitivity secret
- assume `PrivateNode` examples are mainnet-sensitive unless you change the underlying connection logic
- keep read-only workflows on `Indexer` or `PublicNode` whenever possible
