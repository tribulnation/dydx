from typing_extensions import TypeVar, Mapping
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_DOWN, ROUND_FLOOR

D = TypeVar('D', bound=Mapping)

def filter_kwargs(Params: type[D], params: D | dict) -> D:
  return { k: params[k] for k in getattr(Params, '__annotations__', {}) if k in params } # type: ignore

class timestamp:
  @staticmethod
  def parse(time: str) -> datetime:
    return datetime.fromisoformat(time).astimezone()

  @staticmethod
  def dump(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()
  
  @staticmethod
  def now() -> str:
    return timestamp.dump(datetime.now())

def round2tick(x: Decimal, tick_size: Decimal) -> Decimal:
  r = (x / tick_size).quantize(Decimal('1.'), rounding=ROUND_HALF_DOWN) * tick_size
  return r.normalize()

def trunc2tick(x: Decimal, tick_size: Decimal) -> Decimal:
  r = (x / tick_size).to_integral_value(rounding=ROUND_FLOOR) * tick_size
  return r.normalize()

def path_join(base: str, *parts: str):
  return '/'.join([base.rstrip('/')] + [part.lstrip('/') for part in parts])

def getenv(var: str) -> str:
  import os
  try:
    return os.environ[var]
  except KeyError:
    raise ValueError(f'Environment variable {var} not found')
