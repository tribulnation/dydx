from dataclasses import dataclass as _dataclass
from .core import OEGS_GRPC_URL
from .private import PrivateNode
from .public import PublicNode

@_dataclass
class Node(PublicNode, PrivateNode):
  ...
