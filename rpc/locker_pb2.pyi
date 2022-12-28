from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LockReply(_message.Message):
    __slots__ = ["is_success", "message"]
    IS_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    is_success: bool
    message: str
    def __init__(self, is_success: bool = ..., message: _Optional[str] = ...) -> None: ...

class LockRequest(_message.Message):
    __slots__ = ["is_acquire", "token"]
    IS_ACQUIRE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    is_acquire: bool
    token: int
    def __init__(self, is_acquire: bool = ..., token: _Optional[int] = ...) -> None: ...
