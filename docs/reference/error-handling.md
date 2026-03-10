# Error Handling

The main error types in this package are:

- `NetworkError` for HTTP or WebSocket transport failures
- `ValidationError` for schema mismatches
- `ApiError` for indexer or node-level API failures
- `UserError` for invalid local usage

## Recommended Pattern

```python
from dydx.core import ApiError, NetworkError, UserError, ValidationError

try:
  ...
except ValidationError:
  ...
except UserError:
  ...
except ApiError:
  ...
except NetworkError:
  ...
```

## Notes

- indexer HTTP failures are wrapped as `ApiError(status, result)`
- node gRPC failures are also normalized into `ApiError`
- `batch_cancel_orders` may raise `UserError` for unsupported order shapes, such as non-short-term batch cancels
