#!/usr/bin/python3

import warnings

try:
    from pydantic.v1 import BaseModel, validator
except ImportError:
    from pydantic import BaseModel, validator

from typing import List

import dingosdk

index_types = {
    "flat": dingosdk.VectorIndexType.kFlat,
    "ivf_flat": dingosdk.VectorIndexType.kIvfFlat,
    "ivf_pq": dingosdk.VectorIndexType.kIvfPq,
    "hnsw": dingosdk.VectorIndexType.kHnsw,
    "diskann": dingosdk.VectorIndexType.kDiskAnn,
    "brute": dingosdk.VectorIndexType.kBruteForce,
    "binary_flat": dingosdk.VectorIndexType.kBinaryFlat,
    "binary_ivf_flat":dingosdk.VectorIndexType.kBinaryIvfFlat,
}

metric_types = {
    "euclidean": dingosdk.MetricType.kL2,
    "dotproduct": dingosdk.MetricType.kInnerProduct,
    "cosine": dingosdk.MetricType.kCosine,
    "hamming": dingosdk.MetricType.kHamming
}

value_type = {
    "float": dingosdk.ValueType.kFloat,
    "uint8": dingosdk.ValueType.kUint8,
    "int8": dingosdk.ValueType.kInt8,
}

index_params = {
    "flat": {"dimension": None, "metricType": None},
    "ivf_flat": {"dimension": None, "metricType": None, "ncentroids": 256},
    "ivf_pq": {
        "dimension": None,
        "metricType": None,
        "ncentroids": 256,
        "bucketInitSize": 1000,
        "bucketMaxSize": 128000,
        "nsubvector": 8,
        "nbitsPerIdx": 8,
    },
    "hnsw": {
        "dimension": None,
        "metricType": None,
        "efConstruction": 200,
        "maxElements": 50000,
        "nlinks": 32,
    },
    "diskann": {
        "dimension": None,
        "metricType": None,
        "valueType": None,
        "maxDegree": 64,
        "searchListSize": 100,
    },
    "brute": {"dimension": None, "metricType": None},
    "binary_flat":{"dimension": None, "metricType": None},
    "binary_ivf_flat": {"dimension": None, "metricType": None, "ncentroids": 256},
}


class CreateIndexParam(BaseModel):
    index_name: str
    dimension: int
    index_type: str
    metric_type: str
    replicas: int = 3
    index_config: dict = None
    metadata_config: dict = None
    partition_rule: dict = None
    operand: list = None
    auto_id: bool = True
    start_id: int = 1

    @validator("index_type", always=True)
    def check_index_type(cls, value):
        if value not in index_types.keys():
            raise Exception(f"index_type  must in {list(index_types.keys())}")
        return value

    @validator("metric_type", always=True)
    def check_metric_type(cls, value):
        if value not in metric_types.keys():
            raise Exception(f"metric_type  must in {metric_types.keys()}")
        return value

    @validator("replicas", always=True)
    def check_replicas(cls, value):
        if value < 0:
            raise Exception(f"{value} must >= 0")
        if value == 0:
            value = 3
        return value

    @validator("index_config", always=True)
    def check_index_config(cls, value, values):
        index_type = values.get("index_type")

        dimension = values.get("dimension")
        metric_type = values.get("metric_type")

        vector_index_parameter = index_params[index_type]

        if value is not None:
            for key, v in value.items():
                if key in vector_index_parameter.keys():
                    if key == "efConstruction":
                        if v < 0:
                            raise Exception(f"{key} must >= 0")
                        if v > 500 or v < 100:
                            warnings.warn(f"efConstruction: {v} suggestion in 100-500")
                    if key == "maxElements":
                        if v < 0:
                            raise Exception(f"{key} must >= 0")
                        if v > 1000000000 or v < 50000:
                            warnings.warn(
                                f"maxElements:{v} suggestion in 50000-1000000000"
                            )
                    if key == "nlinks":
                        if v < 0:
                            raise Exception(f"{key} must >= 0")
                        if v > 64 or v < 16:
                            warnings.warn(f"nlinks:{v} suggestion in 16-64")

                    if key == "nsubvector":
                        if dimension % v != 0:
                            raise Exception(f"dimension/nsubvector must Divisible")
                        if v <= 0:
                            raise Exception(f"{key} must > 0")
                        if v > 256 or v < 4:
                            warnings.warn(f"nsubvector:{v} suggestion in 4-256")
                    if key == "ncentroids":
                        if v <= 0:
                            raise Exception(f"{key} must > 0")
                        if v > 4096 or v < 4:
                            warnings.warn(f"ncentroids:{v} suggestion in 4-4096")
                    if key == "bucketInitSize":
                        if v <= 0:
                            raise Exception(f"{key} must > 0")
                    if key == "bucketMaxSize":
                        if v <= 0:
                            raise Exception(f"{key} must > 0")
                    if key == "nbitsPerIdx":
                        if v <= 0 or v > 16:
                            raise Exception(f"{key} must > 0 and <=16")
                    if key == "maxDegree":
                        if v < 60 or v > 150:
                            raise Exception(f"{key} must >= 60 and <=150")
                    if key == "searchListSize":
                        if v < 75 or v > 200:
                            raise Exception(f"{key} must >= 75 and <=200")
                    if key == "valueType":
                        if v != "float":
                            raise Exception(f"{key} must == float")
                        vector_index_parameter[key] = value_type.get(v)
                        continue
                    vector_index_parameter[key] = v
                else:
                    warnings.warn(f"index_config {key} not in {index_type}")

        vector_index_parameter["dimension"] = dimension
        vector_index_parameter["metricType"] = metric_types[metric_type]

        return vector_index_parameter

    @validator("partition_rule", always=True)
    def check_partition_rule(cls, value):
        value = {} if value is None else value
        if len(value) != 0:
            raise RuntimeError("partition_rule is not support now")
        return value

    @validator("metadata_config", always=True)
    def check_metadata_config(cls, value):
        value = {} if value is None else value
        if len(value) != 0:
            raise RuntimeError("metadata_config is not support now")

    @validator("start_id", always=True)
    def check_start_id(cls, value, values):
        auto_id = values.get("auto_id")
        if auto_id:
            if value < 1:
                raise Exception(f"start_id must >= 1")
        return value


class VectorAddParam(BaseModel):
    index_name: str
    vectors: List[list]
    datas: List[dict] = None
    ids: List[int] = None
    value_type: str = "float"

    @validator("value_type", always=True)
    def check_value_type(cls, value, values):
        if value is None:
            value = "float"  
        if value not in {"binary", "float"}:
            raise Exception("value_type must be 'binary' or 'float'")
        return value

    @validator("datas", always=True)
    def check_datas(cls, value, values):
        value = [{}] * len(values.get("vectors")) if value is None else value
        return value

    @validator("ids", always=True)
    def check_ids(cls, value, values):
        if value is None:
            assert len(values.get("datas")) == len(
                values.get("vectors")
            ), f"length datas:{len(values.get('datas'))} vectors: {len(values.get('vectors'))} is not equal"
        else:
            assert (
                len(values.get("datas")) == len(values.get("vectors")) == len(value)
            ), f"length datas:{len(values.get('datas'))} vectors: {len(values.get('vectors'))} ids:{len(value)} is not equal"
            for id in value:
                if id <= 0:
                    raise Exception("id must > 0")
        return value

class VectorScanParam(BaseModel):
    index_name: str
    start_id: int
    max_count: int = 1000
    is_reverse: bool = False
    with_scalar_data: bool = True
    with_table_data: bool = True
    with_vector_data: bool = True
    fields: list = None
    filter_scalar: dict = None
    end_id: int = 0

    @validator("end_id", pre=True, always=True)
    def check_true_positive_values(cls, value, field):
        if not value >= 0:
            raise ValueError(f"{field.name} must >= 0")
        return value

    @validator("start_id", "max_count", pre=True, always=True)
    def check_positive_values(cls, value, field):
        if not value > 0:
            raise ValueError(f"{field.name} must > 0")
        return value

    @validator("fields", pre=True, always=True)
    def check_fields(cls, value):
        return value or []

    @validator("filter_scalar", pre=True, always=True)
    def check_filter_scalar(cls, value):
        if value is None:
            return {}
        else:
            return value


class VectorSearchParam(BaseModel):
    index_name: str
    xq: list
    top_k: int
    fields: list = None  # select keys
    pre_filter: bool = True
    brute: bool = False
    search_params: dict = None
    with_vector_data: bool = True
    with_scalar_data: bool = True
    beamwidth: int = 2
    value_type: str="float"

    @validator("value_type", always=True)
    def check_value_type(cls, value, values):
        if value is None:
            value = "float"  
        if value not in {"binary", "float"}:
            raise Exception("value_type must be 'binary' or 'float'")
        return value

    @validator("xq", always=True)
    def check_xq(cls, value):
        if not isinstance(value[0], list):
            value = [value]
        return value

    @validator("top_k", pre=True, always=True)
    def check_top_k(cls, value, field):
        if not value > 0:
            raise ValueError(f"{field.name} must > 0")
        return value

    @validator("fields", always=True)
    def check_fields(cls, value):
        if value is None:
            value = []
        return value

    @validator("search_params", always=True)
    def check_search_params(cls, search_params, values):
        if search_params is None or len(search_params) == 0:
            search_params = {}
            values["pre_filter"] = False
            return search_params

        assert search_params is not None, "search_params is None"

        values["with_vector_data"] = search_params.get("withVectorData", True)
        values["with_scalar_data"] = search_params.get("withScalarData", True)

        if (
            "meta_expr" in search_params.keys()
            and "langchain_expr" in search_params.keys()
        ):
            raise ValueError(f"meta_expr and langchain_expr cannot coexist")

        if (
            "meta_expr" not in search_params.keys()
            and "langchain_expr" not in search_params.keys()
        ):
            values["pre_filter"] = False

        return search_params


class VectorGetParam(BaseModel):
    index_name: str
    ids: List[int]
    with_scalar_data: bool = True
    with_vector_data: bool = True

    @validator("ids", always=True)
    def check_ids(cls, value):
        id_list = []
        for id in value:
            if id <= 0:
                raise Exception("id must > 0")
            else:
                id_list.append(id)

        return id_list


class VectorDeleteParam(BaseModel):
    index_name: str
    ids: List[int]

    @validator("ids", always=True)
    def check_ids(cls, value):
        id_list = []
        for id in value:
            if id <= 0:
                raise Exception("id must > 0")
            else:
                id_list.append(id)
        return id_list


class VectorStatusByRegionIdParam(BaseModel):
    index_name: str
    ids: List[int]

    @validator("ids", always=True)
    def check_ids(cls, value):
        id_list = []
        for id in value:
            if id <= 0:
                raise Exception("id must > 0")
            else:
                id_list.append(id)
        return id_list


class VectorBuildByRegionIdParam(BaseModel):
    index_name: str
    ids: List[int]

    @validator("ids", always=True)
    def check_ids(cls, value):
        id_list = []
        for id in value:
            if id <= 0:
                raise Exception("id must > 0")
            else:
                id_list.append(id)
        return id_list


class VectorLoadByRegionIdParam(BaseModel):
    index_name: str
    ids: List[int]

    @validator("ids", always=True)
    def check_ids(cls, value):
        id_list = []
        for id in value:
            if id <= 0:
                raise Exception("id must > 0")
            else:
                id_list.append(id)
        return id_list


class VectorResetByRegionIdParam(BaseModel):
    index_name: str
    ids: List[int]

    @validator("ids", always=True)
    def check_ids(cls, value):
        id_list = []
        for id in value:
            if id <= 0:
                raise Exception("id must > 0")
            else:
                id_list.append(id)
        return id_list
