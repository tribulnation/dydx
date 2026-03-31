# Trading Access

For dYdX, the important distinction is not public vs API-key access. It is indexer vs node access.

## Public Usage

No credentials are required for:

- `Indexer`
- `PublicNode`

Use these imports for public/read-only workflows:

```python
from dydx import Indexer
from dydx.node import PublicNode
```

## Private Trading Setup

`DYDX` and `PrivateNode` currently use mnemonic-based access.

```bash
export DYDX_MNEMONIC="your twelve or twenty-four word mnemonic"
export DYDX_TESTNET_MNEMONIC="your testnet twelve or twenty-four word mnemonic"
```

```python
from dydx import DYDX

dydx = DYDX.new(mnemonic="your mnemonic here")
```

## Security Notes

- never commit your mnemonic
- treat `DYDX_MNEMONIC` and `DYDX_TESTNET_MNEMONIC` as high-sensitivity secrets
- assume `DYDX` and `PrivateNode` examples are mainnet-sensitive unless you change the underlying connection logic
- keep read-only workflows on `Indexer` or `PublicNode` whenever possible
