from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    FLOAT: _ClassVar[ValueType]
    UINT8: _ClassVar[ValueType]

class ScalarIndexType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    SCALAR_INDEX_TYPE_NONE: _ClassVar[ScalarIndexType]
    SCALAR_INDEX_TYPE_LSM: _ClassVar[ScalarIndexType]
    SCALAR_INDEX_TYPE_BTREE: _ClassVar[ScalarIndexType]

class IndexType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    INDEX_TYPE_NONE: _ClassVar[IndexType]
    INDEX_TYPE_VECTOR: _ClassVar[IndexType]
    INDEX_TYPE_SCALAR: _ClassVar[IndexType]

class VectorIndexType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    VECTOR_INDEX_TYPE_NONE: _ClassVar[VectorIndexType]
    VECTOR_INDEX_TYPE_FLAT: _ClassVar[VectorIndexType]
    VECTOR_INDEX_TYPE_IVF_FLAT: _ClassVar[VectorIndexType]
    VECTOR_INDEX_TYPE_IVF_PQ: _ClassVar[VectorIndexType]
    VECTOR_INDEX_TYPE_HNSW: _ClassVar[VectorIndexType]
    VECTOR_INDEX_TYPE_DISKANN: _ClassVar[VectorIndexType]
    VECTOR_INDEX_TYPE_BRUTEFORCE: _ClassVar[VectorIndexType]

class MetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    METRIC_TYPE_NONE: _ClassVar[MetricType]
    METRIC_TYPE_L2: _ClassVar[MetricType]
    METRIC_TYPE_INNER_PRODUCT: _ClassVar[MetricType]
    METRIC_TYPE_COSINE: _ClassVar[MetricType]

class VectorFilter(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    SCALAR_FILTER: _ClassVar[VectorFilter]
    TABLE_FILTER: _ClassVar[VectorFilter]
    VECTOR_ID_FILTER: _ClassVar[VectorFilter]

class VectorFilterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    QUERY_POST: _ClassVar[VectorFilterType]
    QUERY_PRE: _ClassVar[VectorFilterType]

class ScalarFieldType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    NONE: _ClassVar[ScalarFieldType]
    BOOL: _ClassVar[ScalarFieldType]
    INT8: _ClassVar[ScalarFieldType]
    INT16: _ClassVar[ScalarFieldType]
    INT32: _ClassVar[ScalarFieldType]
    INT64: _ClassVar[ScalarFieldType]
    FLOAT32: _ClassVar[ScalarFieldType]
    DOUBLE: _ClassVar[ScalarFieldType]
    STRING: _ClassVar[ScalarFieldType]
    BYTES: _ClassVar[ScalarFieldType]
FLOAT: ValueType
UINT8: ValueType
SCALAR_INDEX_TYPE_NONE: ScalarIndexType
SCALAR_INDEX_TYPE_LSM: ScalarIndexType
SCALAR_INDEX_TYPE_BTREE: ScalarIndexType
INDEX_TYPE_NONE: IndexType
INDEX_TYPE_VECTOR: IndexType
INDEX_TYPE_SCALAR: IndexType
VECTOR_INDEX_TYPE_NONE: VectorIndexType
VECTOR_INDEX_TYPE_FLAT: VectorIndexType
VECTOR_INDEX_TYPE_IVF_FLAT: VectorIndexType
VECTOR_INDEX_TYPE_IVF_PQ: VectorIndexType
VECTOR_INDEX_TYPE_HNSW: VectorIndexType
VECTOR_INDEX_TYPE_DISKANN: VectorIndexType
VECTOR_INDEX_TYPE_BRUTEFORCE: VectorIndexType
METRIC_TYPE_NONE: MetricType
METRIC_TYPE_L2: MetricType
METRIC_TYPE_INNER_PRODUCT: MetricType
METRIC_TYPE_COSINE: MetricType
SCALAR_FILTER: VectorFilter
TABLE_FILTER: VectorFilter
VECTOR_ID_FILTER: VectorFilter
QUERY_POST: VectorFilterType
QUERY_PRE: VectorFilterType
NONE: ScalarFieldType
BOOL: ScalarFieldType
INT8: ScalarFieldType
INT16: ScalarFieldType
INT32: ScalarFieldType
INT64: ScalarFieldType
FLOAT32: ScalarFieldType
DOUBLE: ScalarFieldType
STRING: ScalarFieldType
BYTES: ScalarFieldType

class ColumnDefinition(_message.Message):
    __slots__ = ["name", "sql_type", "element_type", "precision", "scale", "nullable", "indexOfKey", "has_default_val", "default_val"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SQL_TYPE_FIELD_NUMBER: _ClassVar[int]
    ELEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    NULLABLE_FIELD_NUMBER: _ClassVar[int]
    INDEXOFKEY_FIELD_NUMBER: _ClassVar[int]
    HAS_DEFAULT_VAL_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VAL_FIELD_NUMBER: _ClassVar[int]
    name: str
    sql_type: str
    element_type: str
    precision: int
    scale: int
    nullable: bool
    indexOfKey: int
    has_default_val: bool
    default_val: str
    def __init__(self, name: _Optional[str] = ..., sql_type: _Optional[str] = ..., element_type: _Optional[str] = ..., precision: _Optional[int] = ..., scale: _Optional[int] = ..., nullable: bool = ..., indexOfKey: _Optional[int] = ..., has_default_val: bool = ..., default_val: _Optional[str] = ...) -> None: ...

class Vector(_message.Message):
    __slots__ = ["dimension", "value_type", "float_values", "binary_values"]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUES_FIELD_NUMBER: _ClassVar[int]
    BINARY_VALUES_FIELD_NUMBER: _ClassVar[int]
    dimension: int
    value_type: ValueType
    float_values: _containers.RepeatedScalarFieldContainer[float]
    binary_values: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, dimension: _Optional[int] = ..., value_type: _Optional[_Union[ValueType, str]] = ..., float_values: _Optional[_Iterable[float]] = ..., binary_values: _Optional[_Iterable[bytes]] = ...) -> None: ...

class VectorScalarData(_message.Message):
    __slots__ = ["scalar_data"]
    class ScalarDataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ScalarValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ScalarValue, _Mapping]] = ...) -> None: ...
    SCALAR_DATA_FIELD_NUMBER: _ClassVar[int]
    scalar_data: _containers.MessageMap[str, ScalarValue]
    def __init__(self, scalar_data: _Optional[_Mapping[str, ScalarValue]] = ...) -> None: ...

class VectorTableData(_message.Message):
    __slots__ = ["table_key", "table_value"]
    TABLE_KEY_FIELD_NUMBER: _ClassVar[int]
    TABLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    table_key: bytes
    table_value: bytes
    def __init__(self, table_key: _Optional[bytes] = ..., table_value: _Optional[bytes] = ...) -> None: ...

class VectorWithId(_message.Message):
    __slots__ = ["id", "vector", "scalar_data", "table_data"]
    class ScalarDataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ScalarValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ScalarValue, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    SCALAR_DATA_FIELD_NUMBER: _ClassVar[int]
    TABLE_DATA_FIELD_NUMBER: _ClassVar[int]
    id: int
    vector: Vector
    scalar_data: _containers.MessageMap[str, ScalarValue]
    table_data: VectorTableData
    def __init__(self, id: _Optional[int] = ..., vector: _Optional[_Union[Vector, _Mapping]] = ..., scalar_data: _Optional[_Mapping[str, ScalarValue]] = ..., table_data: _Optional[_Union[VectorTableData, _Mapping]] = ...) -> None: ...

class VectorWithDistance(_message.Message):
    __slots__ = ["id", "vector", "scalar_data", "distance", "metric_type"]
    class ScalarDataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ScalarValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ScalarValue, _Mapping]] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    SCALAR_DATA_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    vector: Vector
    scalar_data: _containers.MessageMap[str, ScalarValue]
    distance: float
    metric_type: MetricType
    def __init__(self, id: _Optional[int] = ..., vector: _Optional[_Union[Vector, _Mapping]] = ..., scalar_data: _Optional[_Mapping[str, ScalarValue]] = ..., distance: _Optional[float] = ..., metric_type: _Optional[_Union[MetricType, str]] = ...) -> None: ...

class IndexParameter(_message.Message):
    __slots__ = ["index_type", "vector_index_parameter", "scalar_index_parameter"]
    INDEX_TYPE_FIELD_NUMBER: _ClassVar[int]
    VECTOR_INDEX_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    SCALAR_INDEX_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    index_type: IndexType
    vector_index_parameter: VectorIndexParameter
    scalar_index_parameter: ScalarIndexParameter
    def __init__(self, index_type: _Optional[_Union[IndexType, str]] = ..., vector_index_parameter: _Optional[_Union[VectorIndexParameter, _Mapping]] = ..., scalar_index_parameter: _Optional[_Union[ScalarIndexParameter, _Mapping]] = ...) -> None: ...

class CreateFlatParam(_message.Message):
    __slots__ = ["dimension", "metric_type"]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    dimension: int
    metric_type: MetricType
    def __init__(self, dimension: _Optional[int] = ..., metric_type: _Optional[_Union[MetricType, str]] = ...) -> None: ...

class CreateIvfFlatParam(_message.Message):
    __slots__ = ["dimension", "metric_type", "ncentroids"]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    NCENTROIDS_FIELD_NUMBER: _ClassVar[int]
    dimension: int
    metric_type: MetricType
    ncentroids: int
    def __init__(self, dimension: _Optional[int] = ..., metric_type: _Optional[_Union[MetricType, str]] = ..., ncentroids: _Optional[int] = ...) -> None: ...

class CreateIvfPqParam(_message.Message):
    __slots__ = ["dimension", "metric_type", "ncentroids", "nsubvector", "bucket_init_size", "bucket_max_size", "nbits_per_idx"]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    NCENTROIDS_FIELD_NUMBER: _ClassVar[int]
    NSUBVECTOR_FIELD_NUMBER: _ClassVar[int]
    BUCKET_INIT_SIZE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_MAX_SIZE_FIELD_NUMBER: _ClassVar[int]
    NBITS_PER_IDX_FIELD_NUMBER: _ClassVar[int]
    dimension: int
    metric_type: MetricType
    ncentroids: int
    nsubvector: int
    bucket_init_size: int
    bucket_max_size: int
    nbits_per_idx: int
    def __init__(self, dimension: _Optional[int] = ..., metric_type: _Optional[_Union[MetricType, str]] = ..., ncentroids: _Optional[int] = ..., nsubvector: _Optional[int] = ..., bucket_init_size: _Optional[int] = ..., bucket_max_size: _Optional[int] = ..., nbits_per_idx: _Optional[int] = ...) -> None: ...

class CreateHnswParam(_message.Message):
    __slots__ = ["dimension", "metric_type", "efConstruction", "max_elements", "nlinks"]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    EFCONSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    MAX_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    NLINKS_FIELD_NUMBER: _ClassVar[int]
    dimension: int
    metric_type: MetricType
    efConstruction: int
    max_elements: int
    nlinks: int
    def __init__(self, dimension: _Optional[int] = ..., metric_type: _Optional[_Union[MetricType, str]] = ..., efConstruction: _Optional[int] = ..., max_elements: _Optional[int] = ..., nlinks: _Optional[int] = ...) -> None: ...

class CreateDiskAnnParam(_message.Message):
    __slots__ = ["dimension", "metric_type", "num_trees", "num_neighbors", "num_threads"]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    NUM_TREES_FIELD_NUMBER: _ClassVar[int]
    NUM_NEIGHBORS_FIELD_NUMBER: _ClassVar[int]
    NUM_THREADS_FIELD_NUMBER: _ClassVar[int]
    dimension: int
    metric_type: MetricType
    num_trees: int
    num_neighbors: int
    num_threads: int
    def __init__(self, dimension: _Optional[int] = ..., metric_type: _Optional[_Union[MetricType, str]] = ..., num_trees: _Optional[int] = ..., num_neighbors: _Optional[int] = ..., num_threads: _Optional[int] = ...) -> None: ...

class CreateBruteForceParam(_message.Message):
    __slots__ = ["dimension", "metric_type"]
    DIMENSION_FIELD_NUMBER: _ClassVar[int]
    METRIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    dimension: int
    metric_type: MetricType
    def __init__(self, dimension: _Optional[int] = ..., metric_type: _Optional[_Union[MetricType, str]] = ...) -> None: ...

class VectorIndexParameter(_message.Message):
    __slots__ = ["vector_index_type", "flat_parameter", "ivf_flat_parameter", "ivf_pq_parameter", "hnsw_parameter", "diskann_parameter", "bruteforce_parameter"]
    VECTOR_INDEX_TYPE_FIELD_NUMBER: _ClassVar[int]
    FLAT_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    IVF_FLAT_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    IVF_PQ_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    HNSW_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    DISKANN_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    BRUTEFORCE_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    vector_index_type: VectorIndexType
    flat_parameter: CreateFlatParam
    ivf_flat_parameter: CreateIvfFlatParam
    ivf_pq_parameter: CreateIvfPqParam
    hnsw_parameter: CreateHnswParam
    diskann_parameter: CreateDiskAnnParam
    bruteforce_parameter: CreateBruteForceParam
    def __init__(self, vector_index_type: _Optional[_Union[VectorIndexType, str]] = ..., flat_parameter: _Optional[_Union[CreateFlatParam, _Mapping]] = ..., ivf_flat_parameter: _Optional[_Union[CreateIvfFlatParam, _Mapping]] = ..., ivf_pq_parameter: _Optional[_Union[CreateIvfPqParam, _Mapping]] = ..., hnsw_parameter: _Optional[_Union[CreateHnswParam, _Mapping]] = ..., diskann_parameter: _Optional[_Union[CreateDiskAnnParam, _Mapping]] = ..., bruteforce_parameter: _Optional[_Union[CreateBruteForceParam, _Mapping]] = ...) -> None: ...

class VectorSchema(_message.Message):
    __slots__ = ["type", "is_key", "is_nullable", "index"]
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        BOOL: _ClassVar[VectorSchema.Type]
        INTEGER: _ClassVar[VectorSchema.Type]
        FLOAT: _ClassVar[VectorSchema.Type]
        LONG: _ClassVar[VectorSchema.Type]
        DOUBLE: _ClassVar[VectorSchema.Type]
        STRING: _ClassVar[VectorSchema.Type]
    BOOL: VectorSchema.Type
    INTEGER: VectorSchema.Type
    FLOAT: VectorSchema.Type
    LONG: VectorSchema.Type
    DOUBLE: VectorSchema.Type
    STRING: VectorSchema.Type
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IS_KEY_FIELD_NUMBER: _ClassVar[int]
    IS_NULLABLE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    type: VectorSchema.Type
    is_key: bool
    is_nullable: bool
    index: int
    def __init__(self, type: _Optional[_Union[VectorSchema.Type, str]] = ..., is_key: bool = ..., is_nullable: bool = ..., index: _Optional[int] = ...) -> None: ...

class ScalarIndexParameter(_message.Message):
    __slots__ = ["scalar_index_type"]
    SCALAR_INDEX_TYPE_FIELD_NUMBER: _ClassVar[int]
    scalar_index_type: ScalarIndexType
    def __init__(self, scalar_index_type: _Optional[_Union[ScalarIndexType, str]] = ...) -> None: ...

class SearchFlatParam(_message.Message):
    __slots__ = ["parallel_on_queries"]
    PARALLEL_ON_QUERIES_FIELD_NUMBER: _ClassVar[int]
    parallel_on_queries: int
    def __init__(self, parallel_on_queries: _Optional[int] = ...) -> None: ...

class SearchIvfFlatParam(_message.Message):
    __slots__ = ["nprobe", "parallel_on_queries"]
    NPROBE_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_ON_QUERIES_FIELD_NUMBER: _ClassVar[int]
    nprobe: int
    parallel_on_queries: int
    def __init__(self, nprobe: _Optional[int] = ..., parallel_on_queries: _Optional[int] = ...) -> None: ...

class SearchIvfPqParam(_message.Message):
    __slots__ = ["nprobe", "parallel_on_queries", "recall_num"]
    NPROBE_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_ON_QUERIES_FIELD_NUMBER: _ClassVar[int]
    RECALL_NUM_FIELD_NUMBER: _ClassVar[int]
    nprobe: int
    parallel_on_queries: int
    recall_num: int
    def __init__(self, nprobe: _Optional[int] = ..., parallel_on_queries: _Optional[int] = ..., recall_num: _Optional[int] = ...) -> None: ...

class SearchHNSWParam(_message.Message):
    __slots__ = ["efSearch"]
    EFSEARCH_FIELD_NUMBER: _ClassVar[int]
    efSearch: int
    def __init__(self, efSearch: _Optional[int] = ...) -> None: ...

class SearchDiskAnnParam(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class VectorSearchParameter(_message.Message):
    __slots__ = ["top_n", "without_vector_data", "without_scalar_data", "selected_keys", "without_table_data", "flat", "ivf_flat", "ivf_pq", "hnsw", "diskann", "use_scalar_filter", "vector_filter", "vector_filter_type", "vector_coprocessor", "vector_ids", "use_brute_force"]
    TOP_N_FIELD_NUMBER: _ClassVar[int]
    WITHOUT_VECTOR_DATA_FIELD_NUMBER: _ClassVar[int]
    WITHOUT_SCALAR_DATA_FIELD_NUMBER: _ClassVar[int]
    SELECTED_KEYS_FIELD_NUMBER: _ClassVar[int]
    WITHOUT_TABLE_DATA_FIELD_NUMBER: _ClassVar[int]
    FLAT_FIELD_NUMBER: _ClassVar[int]
    IVF_FLAT_FIELD_NUMBER: _ClassVar[int]
    IVF_PQ_FIELD_NUMBER: _ClassVar[int]
    HNSW_FIELD_NUMBER: _ClassVar[int]
    DISKANN_FIELD_NUMBER: _ClassVar[int]
    USE_SCALAR_FILTER_FIELD_NUMBER: _ClassVar[int]
    VECTOR_FILTER_FIELD_NUMBER: _ClassVar[int]
    VECTOR_FILTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    VECTOR_COPROCESSOR_FIELD_NUMBER: _ClassVar[int]
    VECTOR_IDS_FIELD_NUMBER: _ClassVar[int]
    USE_BRUTE_FORCE_FIELD_NUMBER: _ClassVar[int]
    top_n: int
    without_vector_data: bool
    without_scalar_data: bool
    selected_keys: _containers.RepeatedScalarFieldContainer[str]
    without_table_data: bool
    flat: SearchFlatParam
    ivf_flat: SearchIvfFlatParam
    ivf_pq: SearchIvfPqParam
    hnsw: SearchHNSWParam
    diskann: SearchDiskAnnParam
    use_scalar_filter: bool
    vector_filter: VectorFilter
    vector_filter_type: VectorFilterType
    vector_coprocessor: VectorCoprocessor
    vector_ids: _containers.RepeatedScalarFieldContainer[int]
    use_brute_force: bool
    def __init__(self, top_n: _Optional[int] = ..., without_vector_data: bool = ..., without_scalar_data: bool = ..., selected_keys: _Optional[_Iterable[str]] = ..., without_table_data: bool = ..., flat: _Optional[_Union[SearchFlatParam, _Mapping]] = ..., ivf_flat: _Optional[_Union[SearchIvfFlatParam, _Mapping]] = ..., ivf_pq: _Optional[_Union[SearchIvfPqParam, _Mapping]] = ..., hnsw: _Optional[_Union[SearchHNSWParam, _Mapping]] = ..., diskann: _Optional[_Union[SearchDiskAnnParam, _Mapping]] = ..., use_scalar_filter: bool = ..., vector_filter: _Optional[_Union[VectorFilter, str]] = ..., vector_filter_type: _Optional[_Union[VectorFilterType, str]] = ..., vector_coprocessor: _Optional[_Union[VectorCoprocessor, _Mapping]] = ..., vector_ids: _Optional[_Iterable[int]] = ..., use_brute_force: bool = ...) -> None: ...

class VectorCoprocessor(_message.Message):
    __slots__ = ["schema_version", "original_schema", "selection_columns", "expression"]
    SCHEMA_VERSION_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    SELECTION_COLUMNS_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    schema_version: int
    original_schema: VectorSchemaWrapper
    selection_columns: _containers.RepeatedScalarFieldContainer[int]
    expression: bytes
    def __init__(self, schema_version: _Optional[int] = ..., original_schema: _Optional[_Union[VectorSchemaWrapper, _Mapping]] = ..., selection_columns: _Optional[_Iterable[int]] = ..., expression: _Optional[bytes] = ...) -> None: ...

class VectorSchemaWrapper(_message.Message):
    __slots__ = ["schema", "common_id"]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    COMMON_ID_FIELD_NUMBER: _ClassVar[int]
    schema: _containers.RepeatedCompositeFieldContainer[ColumnDefinition]
    common_id: int
    def __init__(self, schema: _Optional[_Iterable[_Union[ColumnDefinition, _Mapping]]] = ..., common_id: _Optional[int] = ...) -> None: ...

class ScalarField(_message.Message):
    __slots__ = ["bool_data", "int_data", "long_data", "float_data", "double_data", "string_data", "bytes_data"]
    BOOL_DATA_FIELD_NUMBER: _ClassVar[int]
    INT_DATA_FIELD_NUMBER: _ClassVar[int]
    LONG_DATA_FIELD_NUMBER: _ClassVar[int]
    FLOAT_DATA_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_DATA_FIELD_NUMBER: _ClassVar[int]
    STRING_DATA_FIELD_NUMBER: _ClassVar[int]
    BYTES_DATA_FIELD_NUMBER: _ClassVar[int]
    bool_data: bool
    int_data: int
    long_data: int
    float_data: float
    double_data: float
    string_data: str
    bytes_data: bytes
    def __init__(self, bool_data: bool = ..., int_data: _Optional[int] = ..., long_data: _Optional[int] = ..., float_data: _Optional[float] = ..., double_data: _Optional[float] = ..., string_data: _Optional[str] = ..., bytes_data: _Optional[bytes] = ...) -> None: ...

class ScalarValue(_message.Message):
    __slots__ = ["field_type", "fields"]
    FIELD_TYPE_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    field_type: ScalarFieldType
    fields: _containers.RepeatedCompositeFieldContainer[ScalarField]
    def __init__(self, field_type: _Optional[_Union[ScalarFieldType, str]] = ..., fields: _Optional[_Iterable[_Union[ScalarField, _Mapping]]] = ...) -> None: ...

class VectorIndexMetrics(_message.Message):
    __slots__ = ["vector_index_type", "current_count", "deleted_count", "max_id", "min_id", "memory_bytes"]
    VECTOR_INDEX_TYPE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    DELETED_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_ID_FIELD_NUMBER: _ClassVar[int]
    MIN_ID_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_FIELD_NUMBER: _ClassVar[int]
    vector_index_type: VectorIndexType
    current_count: int
    deleted_count: int
    max_id: int
    min_id: int
    memory_bytes: int
    def __init__(self, vector_index_type: _Optional[_Union[VectorIndexType, str]] = ..., current_count: _Optional[int] = ..., deleted_count: _Optional[int] = ..., max_id: _Optional[int] = ..., min_id: _Optional[int] = ..., memory_bytes: _Optional[int] = ...) -> None: ...
