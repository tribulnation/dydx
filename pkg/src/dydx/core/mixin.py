from typing_extensions import TypeVar, TypedDict
import os
from dataclasses import dataclass

from .http import AuthHttpMixin, AuthHttpClient

T = TypeVar('T')

DYDX_API_URL = 'https://api.name.com'

@dataclass
class Endpoint(AuthHttpMixin):
  base_url: str = DYDX_API_URL
  validate: bool = True

  def should_validate(self, validate_param: bool | None = None) -> bool:
    return self.validate if validate_param is None else validate_param

  @classmethod
  def new(
    cls, api_key: str | None = None, api_secret: str | None = None, *,
    base_url: str = DYDX_API_URL, validate: bool = True,
  ):
    if api_key is None:
      api_key = os.environ['NAME_API_KEY']
    if api_secret is None:
      api_secret = os.environ['NAME_SECRET_KEY']
    client = AuthHttpClient(api_key=api_key, api_secret=api_secret)
    return cls(base_url=base_url, http=client, validate=validate)

  @classmethod
  def public(cls, *, base_url: str = DYDX_API_URL, validate: bool = True):
    return cls.new('', '', base_url=base_url, validate=validate)

@dataclass
class Router(Endpoint):
  def __post_init__(self):
    for field, cls in self.__annotations__.items():
      if issubclass(cls, Endpoint) or issubclass(cls, Router):
        setattr(self, field, cls(base_url=self.base_url, http=self.http, validate=self.validate))
