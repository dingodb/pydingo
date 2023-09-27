import proxy_common_pb2 as _proxy_common_pb2
import proxy_error_pb2 as _proxy_error_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VectorAddRequest(_message.Message):
    __slots__ = ["schema_name", "index_name", "vectors", "replace_deleted", "is_update"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    VECTORS_FIELD_NUMBER: _ClassVar[int]
    REPLACE_DELETED_FIELD_NUMBER: _ClassVar[int]
    IS_UPDATE_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    vectors: _containers.RepeatedCompositeFieldContainer[_proxy_common_pb2.VectorWithId]
    replace_deleted: bool
    is_update: bool
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ..., vectors: _Optional[_Iterable[_Union[_proxy_common_pb2.VectorWithId, _Mapping]]] = ..., replace_deleted: bool = ..., is_update: bool = ...) -> None: ...

class VectorAddResponse(_message.Message):
    __slots__ = ["error", "vectors"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VECTORS_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    vectors: _containers.RepeatedCompositeFieldContainer[_proxy_common_pb2.VectorWithId]
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., vectors: _Optional[_Iterable[_Union[_proxy_common_pb2.VectorWithId, _Mapping]]] = ...) -> None: ...

class VectorGetRequest(_message.Message):
    __slots__ = ["schema_name", "index_name", "vector_ids", "without_vector_data", "without_scalar_data", "selected_keys", "without_table_data"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    VECTOR_IDS_FIELD_NUMBER: _ClassVar[int]
    WITHOUT_VECTOR_DATA_FIELD_NUMBER: _ClassVar[int]
    WITHOUT_SCALAR_DATA_FIELD_NUMBER: _ClassVar[int]
    SELECTED_KEYS_FIELD_NUMBER: _ClassVar[int]
    WITHOUT_TABLE_DATA_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    vector_ids: _containers.RepeatedScalarFieldContainer[int]
    without_vector_data: bool
    without_scalar_data: bool
    selected_keys: _containers.RepeatedScalarFieldContainer[str]
    without_table_data: bool
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ..., vector_ids: _Optional[_Iterable[int]] = ..., without_vector_data: bool = ..., without_scalar_data: bool = ..., selected_keys: _Optional[_Iterable[str]] = ..., without_table_data: bool = ...) -> None: ...

class VectorGetResponse(_message.Message):
    __slots__ = ["error", "vectors"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VECTORS_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    vectors: _containers.RepeatedCompositeFieldContainer[_proxy_common_pb2.VectorWithId]
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., vectors: _Optional[_Iterable[_Union[_proxy_common_pb2.VectorWithId, _Mapping]]] = ...) -> None: ...

class VectorSearchRequest(_message.Message):
    __slots__ = ["schema_name", "index_name", "vectors", "parameter"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    VECTORS_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    vectors: _containers.RepeatedCompositeFieldContainer[_proxy_common_pb2.VectorWithId]
    parameter: _proxy_common_pb2.VectorSearchParameter
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ..., vectors: _Optional[_Iterable[_Union[_proxy_common_pb2.VectorWithId, _Mapping]]] = ..., parameter: _Optional[_Union[_proxy_common_pb2.VectorSearchParameter, _Mapping]] = ...) -> None: ...

class VectorWithDistanceResult(_message.Message):
    __slots__ = ["vector_with_distances"]
    VECTOR_WITH_DISTANCES_FIELD_NUMBER: _ClassVar[int]
    vector_with_distances: _containers.RepeatedCompositeFieldContainer[_proxy_common_pb2.VectorWithDistance]
    def __init__(self, vector_with_distances: _Optional[_Iterable[_Union[_proxy_common_pb2.VectorWithDistance, _Mapping]]] = ...) -> None: ...

class VectorSearchResponse(_message.Message):
    __slots__ = ["error", "batch_results"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BATCH_RESULTS_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    batch_results: _containers.RepeatedCompositeFieldContainer[VectorWithDistanceResult]
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., batch_results: _Optional[_Iterable[_Union[VectorWithDistanceResult, _Mapping]]] = ...) -> None: ...

class VectorDeleteRequest(_message.Message):
    __slots__ = ["schema_name", "index_name", "ids"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    IDS_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ..., ids: _Optional[_Iterable[int]] = ...) -> None: ...

class VectorDeleteResponse(_message.Message):
    __slots__ = ["error", "key_states"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    KEY_STATES_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    key_states: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., key_states: _Optional[_Iterable[bool]] = ...) -> None: ...

class VectorGetBorderIdRequest(_message.Message):
    __slots__ = ["schema_name", "index_name", "get_min"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    GET_MIN_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    get_min: bool
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ..., get_min: bool = ...) -> None: ...

class VectorGetBorderIdResponse(_message.Message):
    __slots__ = ["error", "id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    id: int
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., id: _Optional[int] = ...) -> None: ...

class VectorScanQueryRequest(_message.Message):
    __slots__ = ["schema_name", "index_name", "vector_id_start", "is_reverse_scan", "max_scan_count", "vector_id_end", "without_vector_data", "without_scalar_data", "selected_keys", "without_table_data", "use_scalar_filter", "scalar_for_filter"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    VECTOR_ID_START_FIELD_NUMBER: _ClassVar[int]
    IS_REVERSE_SCAN_FIELD_NUMBER: _ClassVar[int]
    MAX_SCAN_COUNT_FIELD_NUMBER: _ClassVar[int]
    VECTOR_ID_END_FIELD_NUMBER: _ClassVar[int]
    WITHOUT_VECTOR_DATA_FIELD_NUMBER: _ClassVar[int]
    WITHOUT_SCALAR_DATA_FIELD_NUMBER: _ClassVar[int]
    SELECTED_KEYS_FIELD_NUMBER: _ClassVar[int]
    WITHOUT_TABLE_DATA_FIELD_NUMBER: _ClassVar[int]
    USE_SCALAR_FILTER_FIELD_NUMBER: _ClassVar[int]
    SCALAR_FOR_FILTER_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    vector_id_start: int
    is_reverse_scan: bool
    max_scan_count: int
    vector_id_end: int
    without_vector_data: bool
    without_scalar_data: bool
    selected_keys: _containers.RepeatedScalarFieldContainer[str]
    without_table_data: bool
    use_scalar_filter: bool
    scalar_for_filter: _proxy_common_pb2.VectorScalarData
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ..., vector_id_start: _Optional[int] = ..., is_reverse_scan: bool = ..., max_scan_count: _Optional[int] = ..., vector_id_end: _Optional[int] = ..., without_vector_data: bool = ..., without_scalar_data: bool = ..., selected_keys: _Optional[_Iterable[str]] = ..., without_table_data: bool = ..., use_scalar_filter: bool = ..., scalar_for_filter: _Optional[_Union[_proxy_common_pb2.VectorScalarData, _Mapping]] = ...) -> None: ...

class VectorScanQueryResponse(_message.Message):
    __slots__ = ["error", "vectors"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VECTORS_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    vectors: _containers.RepeatedCompositeFieldContainer[_proxy_common_pb2.VectorWithId]
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., vectors: _Optional[_Iterable[_Union[_proxy_common_pb2.VectorWithId, _Mapping]]] = ...) -> None: ...

class VectorGetRegionMetricsRequest(_message.Message):
    __slots__ = ["schema_name", "index_name"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ...) -> None: ...

class VectorGetRegionMetricsResponse(_message.Message):
    __slots__ = ["error", "metrics"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    metrics: _proxy_common_pb2.VectorIndexMetrics
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., metrics: _Optional[_Union[_proxy_common_pb2.VectorIndexMetrics, _Mapping]] = ...) -> None: ...

class VectorCountRequest(_message.Message):
    __slots__ = ["schema_name", "index_name"]
    SCHEMA_NAME_FIELD_NUMBER: _ClassVar[int]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    schema_name: str
    index_name: str
    def __init__(self, schema_name: _Optional[str] = ..., index_name: _Optional[str] = ...) -> None: ...

class VectorCountResponse(_message.Message):
    __slots__ = ["error", "count"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    error: _proxy_error_pb2.Error
    count: int
    def __init__(self, error: _Optional[_Union[_proxy_error_pb2.Error, _Mapping]] = ..., count: _Optional[int] = ...) -> None: ...
