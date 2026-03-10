from typing_extensions import TypeVar, Any, Mapping
from dataclasses import dataclass, field
import httpx

from dydx.core import HttpClient, validator, path_join, ApiError

T = TypeVar('T')

def response_parser(type: type[T]):
  val = validator(type)
  def parse_response(r: httpx.Response, *, validate: bool = True) -> T:
    if r.status_code == 200:
      return val(r.text) if validate else r.json()
    else:
      raise ApiError(r.status_code, r.json())
  return parse_response

INDEXER_HTTP_URL = 'https://indexer.dydx.trade/'

@dataclass(kw_only=True)
class IndexerMixin:
  url: str = INDEXER_HTTP_URL
  client: HttpClient = field(default_factory=HttpClient)
  default_validate: bool = True
  
  def validate(self, validate: bool | None = None) -> bool:
    return self.default_validate if validate is None else validate

  async def __aenter__(self):
    await self.client.__aenter__()
    return self
  
  async def __aexit__(self, exc_type, exc_value, traceback):
    await self.client.__aexit__(exc_type, exc_value, traceback)

  async def request(
    self, method: str, path: str,
    *,
    content: httpx._types.RequestContent | None = None,
    data: httpx._types.RequestData | None = None,
    files: httpx._types.RequestFiles | None = None,
    json: Any | None = None,
    params: Mapping[str, Any] | None = None,
    headers: Mapping[str, str] | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault | None = httpx.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx.USE_CLIENT_DEFAULT,
    extensions: httpx._types.RequestExtensions | None = None,
  ):
    url = path_join(self.url, path)
    return await self.client.request(
      method, url, params=params, cookies=cookies, json=json,
      content=content, data=data, files=files, auth=auth, follow_redirects=follow_redirects,
      timeout=timeout, extensions=extensions,
      headers=headers,
    )