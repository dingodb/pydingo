from enum import Enum


class ScalarType(Enum):
    BOOL = "BOOL"
    INT64 = "INT64"
    DOUBLE = "DOUBLE"
    STRING = "STRING"


class VectorValueType(Enum):
    FLOAT = "FLOAT"
    BINARY = "BINARY"


class ScalarColumn:
    def __init__(self, key: str, type: ScalarType, speed: bool = False) -> None:
        self.key = key
        self.type = type
        self.speed = speed


class ScalarSchema:
    def __init__(self):
        self.cols = []

    def add_scalar_column(self, col: ScalarColumn):
        self.cols.append(col)


class ScarlarValue:
    def __init__(self, scalar_type: ScalarType, fields: list):
        self.scalar_type = scalar_type
        self.fields = fields

    def to_dict(self):
        return {"fieldType": self.scalar_type.value, "fields": self.fields}


class ScalarData:
    def __init__(self):
        self.data = {}

    def add_scalar_value(self, key: str, scalar_value: ScarlarValue):
        self.data[key] = scalar_value

    def to_dict(self):
        return {key: value.to_dict() for key, value in self.data.items()}


class Vector:
    def __init__(
        self,
        dimension,
        value_type: VectorValueType,
        float_values: list,
        binary_values: list,
    ):
        self.dimension = dimension
        self.value_type = value_type
        self.float_values = float_values
        self.binary_values = binary_values

    def to_dict(self):
        return {
            "dimension": self.dimension,
            "valueType": self.value_type.value,
            "floatValues": [v for v in self.float_values],
            "binaryValues": [v for v in self.binary_values],
        }


class VectorWithId:
    def __init__(self, id: int, vector: Vector, scalar_data: ScalarData):
        self.id = id
        self.vector = vector
        self.scalar_data = scalar_data

    def to_dict(self):
        return {
            "id": self.id,
            "vector": self.vector.to_dict(),
            "scalarData": self.scalar_data.to_dict(),
        }


class MetricType(Enum):
    L2 = "METRIC_TYPE_L2"
    INNER_PRODUCT = "METRIC_TYPE_INNER_PRODUCT"
    COSINE = "METRIC_TYPE_COSINE"
    HAMMING = "METRIC_TYPE_HAMMING"


class VectorWithDistance:
    def __init__(
        self, vector_with_id: VectorWithId, distance: float, metric_type: MetricType
    ):
        self.vector_with_id = vector_with_id
        self.distance = distance
        self.metric_type = metric_type

    def to_dict(self):
        return {
            "id": self.vector_with_id.id,
            "vector": self.vector_with_id.vector.to_dict(),
            "scalarData": self.vector_with_id.scalar_data.to_dict(),
            "distance": self.distance,
            "metricType": self.metric_type.value,
        }


class SearchResult:
    def __init__(self, vector_with_distance_list: list):
        self.vector_with_distance_list = vector_with_distance_list

    def is_empty(self):
        return len(self.vector_with_distance_list) == 0

    def to_dict(self):
        return {
            "vectorWithDistances": [v.to_dict() for v in self.vector_with_distance_list]
        }


class IndexMetric:
    def __init__(
        self,
        index_type: str,
        count: int,
        deleted_count: int,
        max_vector_id: int,
        min_vector_id: int,
        memory_bytes: int,
    ):
        self.index_type = index_type
        self.count = count
        self.deleted_count = deleted_count
        self.max_vector_id = max_vector_id
        self.min_vector_id = min_vector_id
        self.memory_bytes = memory_bytes

    def to_dict(self):
        return {
            "indexType": self.index_type,
            "count": self.count,
            "deletedCount": self.deleted_count,
            "maxVectorId": self.max_vector_id,
            "minVectorId": self.min_vector_id,
            "memoryBytes": self.memory_bytes,
        }


class RegionStatus:
    def __init__(self, region_id: int, err_msg: str):
        self.region_id = region_id
        self.err_msg = err_msg

    def to_dict(self):
        return {"region_id": self.region_id, "err_msg": self.err_msg}




class RegionState:
    def __init__(self, region_id: int, state: str):
        self.region_id = region_id
        self.state = state

    def to_dict(self):
            return {"region_id ": self.region_id, "region_state": self.state}
      