from typing_extensions import TypedDict, TypeVar, Generic, Literal, Any, Mapping
from dataclasses import dataclass, field
import httpx

from dydx.core import HttpClient, validator, path_join, UserError

T = TypeVar('T')

class OkResponse(TypedDict, Generic[T]):
  status: Literal['OK']
  data: T

class ErrResponse(TypedDict):
  status: Literal['NOT_FOUND', 'BAD_REQUEST']

Response = OkResponse[T] | ErrResponse

def response_parser(type: type[T]):
  val = validator(type)
  def parse_response(r: httpx.Response, *, unsafe: bool = False, validate: bool = True) -> Response[T] | T:
    if r.status_code == 200:
      data = val(r.text) if validate else r.json()
      if unsafe:
        return data
      else:
        return {
          'status': 'OK',
          'data': data,
        }
    else:
      err = r.json()
      if unsafe:
        raise UserError(err)
      else:
        return {
          'status': 'NOT_FOUND' if r.status_code == 404 else 'BAD_REQUEST',
          **err,
        }
  return parse_response

INDEXER_HTTP_URL = 'https://indexer.dydx.trade/'

@dataclass(kw_only=True)
class IndexerMixin:
  url: str = INDEXER_HTTP_URL
  client: HttpClient = field(default_factory=HttpClient)
  default_validate: bool = True
  
  def validate(self, validate: bool | None = None) -> bool:
    return self.default_validate if validate is None else validate

  async def request(
    self, method: str, path: str,
    *,
    content: httpx._types.RequestContent | None = None,
    data: httpx._types.RequestData | None = None,
    files: httpx._types.RequestFiles | None = None,
    json: Any | None = None,
    params: httpx._types.QueryParamTypes | None = None,
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