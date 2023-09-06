import warnings
from typing import List

from dingodb.protos.proxy_common_pb2 import *
from dingodb.protos.proxy_index_pb2 import *
from pydantic import BaseModel, validator

from . import grpc_config as config


class CheckClintParam(BaseModel):
    host: List[str]
    timeout: int


class CheckCreateIndexParam(BaseModel):
    index_name: str
    dimension: int
    index_type: str = "hnsw"
    metric_type: str = "euclidean"
    replicas: int = 3
    index_config: dict = None
    metadata_config: dict = None
    partition_rule: dict = None
    operand: list = None
    auto_id: bool = True
    start_id: int = 1

    @validator("index_type", always=True)
    def check_index_type(cls, value):
        if value not in config.index_config.keys():
            raise Exception(f"index_type  must in {list(config.index_config.keys())}")
        return value

    @validator("metric_type", always=True)
    def check_metric_type(cls, value):
        if value not in config.metric_type.keys():
            raise Exception(f"metric_type  must in {list(config.metric_type.keys())}")
        value = config.metric_type[value]
        return value

    @validator("replicas", always=True)
    def check_replicas(cls, value):
        if value < 0:
            raise Exception(f"{value} must >= 0")
        return value

    @validator("index_config", always=True)
    def check_index_config(cls, value, values):
        index_type = values.get("index_type")
        dimension = values.get("dimension")
        metric_type = values.get("metric_type")
        vector_index_parameter = config.index_config[index_type]

        if value is not None:
            index_keys = vector_index_parameter[
                list(vector_index_parameter.keys())[1]
            ].keys()
            for key, v in value.items():
                if key in index_keys:
                    vector_index_parameter[list(vector_index_parameter.keys())[1]][
                        key
                    ] = v
                    if key == "efConstruction" and (v > 500 or v < 100):
                        if v < 0:
                            raise Exception(f"{key} must >= 0")
                        warnings.warn(f"efConstruction: {v} suggestion in 100-500")
                    if key == "maxElements" and (v > 1000000000 or v < 50000):
                        if v < 0:
                            raise Exception(f"{key} must >= 0")
                        warnings.warn(f"maxElements:{v} suggestion in 50000-1000000000")
                    if key == "nlinks" and (v > 64 or v < 16):
                        if v < 0:
                            raise Exception(f"{key} must >= 0")
                        warnings.warn(f"nlinks:{v} suggestion in 16-64")
                else:
                    warnings.warn(f"index_config {key} not in {index_type}")

        vector_index_parameter[list(vector_index_parameter.keys())[1]][
            "dimension"
        ] = dimension
        vector_index_parameter[list(vector_index_parameter.keys())[1]][
            "metricType"
        ] = metric_type
        return vector_index_parameter

    @validator("partition_rule", always=True)
    def check_partition_rule(cls, value):
        value = {} if value is None else value
        return value


class CheckVectorAddParam(BaseModel):
    index_name: str
    vectors: List[list]
    datas: List[dict] = None
    ids: List[int] = None

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


class CheckVectorScanParam(BaseModel):
    index_name: str
    start_id: int
    max_count: int = 1000
    is_reverse: bool = False
    without_scalar_data: bool = False
    without_table_data: bool = False
    without_vector_data: bool = False
    fields: list = None
    filter_scalar: dict = None
    end_id: int = 0

    @validator("end_id", pre=True, always=True)
    def check_true_positive_values(cls, value):
        if not value >= 0:
            raise ValueError(f"{field.name} must >= 0")
        return value

    @validator("start_id", "max_count", pre=True, always=True)
    def check_positive_values(cls, value, field):
        if not value > 0:
            raise ValueError(f"{field.name} must > 0")
        return value

    @validator("is_reverse", "without_vector_data"", without_scalar_data", "without_table_data", pre=True, always=True)
    def check_boolean_fields(cls, value):
        return "true" if value else "false"
    
    @validator("fields", pre=True, always=True)
    def check_fields(cls, value):
        return value or []

    @validator("filter_scalar", pre=True, always=True)
    def check_filter_scalar(cls, value):
        if value is None:
            return {}
        else:
            scalar_data = dict(
                (key, {"fieldType": "STRING", "fields": [{"data": value}]})
                for key, value in value.items()
            )
            value = scalar_data
            return value


class CheckVectorSearchParam(BaseModel):
    index_name: str
    xq: list
    top_k: int = 10
    fields: list = None
    pre_filter: bool = True
    search_params: dict = None

    @validator("xq", always=True)
    def check_xq(cls, value):
        if not isinstance(value[0], list):
            value = [value]
        return value

    @validator("fields", always=True)
    def check_fields(cls, value):
        if value is None:
            value = []
        return value

    @validator("search_params", always=True)
    def check_search_params(cls, search_params, values):
        parameter = VectorSearchParameter(
            selected_keys=values.get("fields"), top_n=values.get("top_k")
        )

        with_vector_data = (
            True
            if search_params is None
            else search_params.get("withVectorData", True)
        )
        parameter.without_vector_data = False

        
        with_scalar_data = (
            True 
            if search_params is None 
            else search_params.get("withScalarData", True)
        )
        parameter.without_scalar_data = False

        vec_search_request = VectorSearchRequest(
            schema_name="dingo", index_name=values.get("index_name")
        )
        use_scalar_filter = False
        if search_params is not None and "meta_expr" in search_params.keys():
            if search_params["meta_expr"] is not None:
                use_scalar_filter = True
                parameter.vector_filter = SCALAR_FILTER
                parameter.vector_filter_type = (
                    QUERY_PRE if values.get("pre_filter") else QUERY_POST
                )

        parameter.use_scalar_filter = use_scalar_filter
        # scalar_data_map = {}
        for xq in values.get("xq"):
            vec_with_id = VectorWithId(
                vector=Vector(dimension=len(xq), float_values=xq, value_type=FLOAT)
            )
            if use_scalar_filter:
                scalar_data_grpc = VectorScalarData()
                for key, value in search_params["meta_expr"].items():
                    entry = scalar_data_grpc.scalar_data[key]
                    entry.field_type = STRING
                    field = entry.fields.add()
                    field.string_data = value

                vec_with_id.scalar_data.CopyFrom(scalar_data_grpc)
            vec_search_request.vectors.append(vec_with_id)

        ef_search = 32 if search_params is None else search_params.get("efSearch", 32)
        assert ef_search >= 0, f"efSearch must >= 0, but get {ef_search}"

        parameter.hnsw.CopyFrom(SearchHNSWParam(efSearch=ef_search))
        if search_params and "parallelOnQueries" in search_params.keys():
            parameter.flat.CopyFrom(
                SearchFlatParam(
                    parallel_on_queries=0
                    if search_params is None
                    else search_params.get("parallelOnQueries", 0)
                )
            )

        vec_search_request.parameter.CopyFrom(parameter)

        return vec_search_request


class CheckVectorGetParam(BaseModel):
    index_name: str
    ids: List[int]
    scalar: bool = True
    vector: bool = True

    @validator("ids", always=True)
    def check_ids(cls, value):
        id_list = []
        for id in value:
            if id <= 0:
                raise Exception("id must > 0")
            else:
                id_list.append(id)

        return id_list


class CheckVectorDeleteParam(BaseModel):
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
