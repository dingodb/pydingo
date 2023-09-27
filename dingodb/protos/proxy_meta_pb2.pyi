import proxy_common_pb2 as _proxy_common_pb2
import proxy_error_pb2 as _proxy_error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PartitionDetailDefinition(_message.Message):
    __slots__ = ["part_name", "operator", "operand"]
    PART_NAME_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    OPERAND_FIELD_NUMBER: _ClassVar[int]
    part_name: str
    operator: str
    operand: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, part_name: _Optional[str] = ..., operator: _Optional[str] = ..., operand: _Optional[_Iterable[str]] = ...) -> None: ...

class PartitionRule(_message.Message):
    __slots__ = ["func_name", "columns", "details"]
    FUNC_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    func_name: str
    columns: _containers.RepeatedScalarFieldContainer[str]
    details: _containers.RepeatedCompositeFieldContainer[PartitionDetailDefinition]
    def __init__(self, func_name: _Optional[str] = ..., columns: _Optional[_Iterable[str]] = ..., details: _Optional[_Iterable[_Union[PartitionDetailDefinition, _Mapping]]] = ...) -> None: ...

class IndexDefinition(_message.Message):
    __slots__ = ["name", "version", "index_partition", "replica", "index_parameter", "with_auto_increment", "auto_increment"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    INDEX_PARTITION_FIELD_NUMBER: _ClassVar[int]
    REPLICA_FIELD_NUMBER: _ClassVar[int]
    INDEX_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    WITH_AUTO_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    AUTO_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: int
    index_partition: PartitionRule
    replica: int
    index_parameter: _proxy_common_pb2.IndexParameter
    with_auto_increment: bool
    auto_increment: int
    def __init__(self, name: _Optional[str] = ..., version: _Optional[int] = ..., index_partition: _Optional[_Union[PartitionRule, _Mapping]] = ..., replica: _Optional[int] = ..., index_parameter: _Optional[_Union[_proxy_common_pb2.IndexParameter, _Mapping]] = ..., with_auto_increment: bool = ..., auto_increment: _Optional[int] = ...) -> None: ...

class CreateIndexRequest(_message.Message):
    __slots__ = ["schema_name", "definition"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    definition: IndexDefinition
    def __init__(self, schema_name: _Optional[str] = ..., definition: _Optional[_Union[IndexDefinition, _Mapping]] = ...) -> None: ...

class CreateIndexResponse(_message.Message):
    __slots__ = ["error", "state"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    state: bool
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., state: bool = ...) -> None: ...

class UpdateIndexRequest(_message.Message):
    __slots__ = ["schema_name", "definition"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    definition: IndexDefinition
    def __init__(self, schema_name: _Optional[str] = ..., definition: _Optional[_Union[IndexDefinition, _Mapping]] = ...) -> None: ...

class UpdateIndexResponse(_message.Message):
    __slots__ = ["error", "state"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    state: bool
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., state: bool = ...) -> None: ...

class UpdateMaxElementsRequest(_message.Message):
    __slots__ = ["schema_name", "index_name", "max_elements"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    max_elements: int
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ..., max_elements: _Optional[int] = ...) -> None: ...

class UpdateMaxElementsResponse(_message.Message):
    __slots__ = ["error", "state"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    state: bool
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., state: bool = ...) -> None: ...

class DeleteIndexRequest(_message.Message):
    __slots__ = ["schema_name", "index_name"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ...) -> None: ...

class DeleteIndexResponse(_message.Message):
    __slots__ = ["error", "state"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    state: bool
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., state: bool = ...) -> None: ...

class GetIndexRequest(_message.Message):
    __slots__ = ["schema_name", "index_name"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ...) -> None: ...

class GetIndexResponse(_message.Message):
    __slots__ = ["error", "definition"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    definition: IndexDefinition
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., definition: _Optional[_Union[IndexDefinition, _Mapping]] = ...) -> None: ...

class GetIndexesRequest(_message.Message):
    __slots__ = ["schema_name"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    def __init__(self, schema_name: _Optional[str] = ...) -> None: ...

class GetIndexesResponse(_message.Message):
    __slots__ = ["error", "definitions"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DEFINITIONS_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    definitions: _containers.RepeatedCompositeFieldContainer[IndexDefinition]
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., definitions: _Optional[_Iterable[_Union[IndexDefinition, _Mapping]]] = ...) -> None: ...

class GetIndexNamesRequest(_message.Message):
    __slots__ = ["schema_name"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    def __init__(self, schema_name: _Optional[str] = ...) -> None: ...

class GetIndexNamesResponse(_message.Message):
    __slots__ = ["error", "names"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., names: _Optional[_Iterable[str]] = ...) -> None: ...

class GetIndexMetricsRequest(_message.Message):
    __slots__ = ["schema_name", "index_name"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ...) -> None: ...

class GetIndexMetricsResponse(_message.Message):
    __slots__ = ["error", "rows_count", "min_key", "max_key", "part_count", "index_type", "current_count", "deleted_count", "max_id", "min_id", "memory_bytes"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ROWS_COUNT_FIELD_NUMBER: _ClassVar[int]
    MIN_KEY_FIELD_NUMBER: _ClassVar[int]
    MAX_KEY_FIELD_NUMBER: _ClassVar[int]
    PART_COUNT_FIELD_NUMBER: _ClassVar[int]
    INDEX_TYPE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    DELETED_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_ID_FIELD_NUMBER: _ClassVar[int]
    MIN_ID_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    rows_count: int
    min_key: bytes
    max_key: bytes
    part_count: int
    index_type: _proxy_common_pb2.VectorIndexType
    current_count: int
    deleted_count: int
    max_id: int
    min_id: int
    memory_bytes: int
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., rows_count: _Optional[int] = ..., min_key: _Optional[bytes] = ..., max_key: _Optional[bytes] = ..., part_count: _Optional[int] = ..., index_type: _Optional[_Union[_proxy_common_pb2.VectorIndexType, str]] = ..., current_count: _Optional[int] = ..., deleted_count: _Optional[int] = ..., max_id: _Optional[int] = ..., min_id: _Optional[int] = ..., memory_bytes: _Optional[int] = ...) -> None: ...
