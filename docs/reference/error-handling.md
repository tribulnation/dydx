# Error Handling

The main error types in this package are:

- `NetworkError` for HTTP or WebSocket transport failures
- `ValidationError` for schema mismatches
- `ApiError` for indexer or node-level API failures
- `LogicError` for invalid local usage or SDK-side assumptions
- `BadRequest` for invalid request shapes caught by the client or API

## Recommended Pattern

```python
from typed_core.exceptions import ApiError, BadRequest, LogicError, NetworkError, ValidationError

try:
  ...
except ValidationError:
  ...
except BadRequest:
  ...
except LogicError:
  ...
except ApiError:
  ...
except NetworkError:
  ...
```

## Notes

- indexer HTTP failures are wrapped as `ApiError(status, result)`
- node gRPC failures are also normalized into `ApiError`
- `batch_cancel_orders` may raise `BadRequest` for unsupported order shapes, such as non-short-term batch cancels
