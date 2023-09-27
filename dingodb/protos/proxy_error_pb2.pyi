import proxy_common_pb2 as _proxy_common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Errno(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    OK: _ClassVar[Errno]
    EINTERNAL: _ClassVar[Errno]
OK: Errno
EINTERNAL: Errno

class Error(_message.Message):
    __slots__ = ["errcode", "errmsg"]
    ERRCODE_FIELD_NUMBER: _ClassVar[int]
    ERRMSG_FIELD_NUMBER: _ClassVar[int]
    errcode: Errno
    errmsg: str
    def __init__(self, errcode: _Optional[_Union[Errno, str]] = ..., errmsg: _Optional[str] = ...) -> None: ...
