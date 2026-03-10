from typing_extensions import Any

class Error(Exception):
  def __str__(self):
    args = self.args[0] if len(self.args) == 1 else ', '.join(self.args)
    return f'{self.__class__.__name__}({args})'

class NetworkError(Error):
  def __str__(self):
    return super().__str__()

class ValidationError(Error):
  def __str__(self):
    return super().__str__()

class UserError(Error):
  def __str__(self):
    return super().__str__()

class AuthError(Error):
  def __str__(self):
    return super().__str__()

class ApiError(Error):
  def __init__(self, status: Any | None, result, *args):
    super().__init__(result, *args)
    self.status = status
    self.result = result

  def __str__(self):
    return f'{self.__class__.__name__}(status: {self.status}, detail: {self.result})'