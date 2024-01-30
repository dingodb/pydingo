import warnings
from typing import List, Union

from pydantic import BaseModel, validator

from . import config
from dingodb.utils.tools import auto_value_type, auto_expr_type


class CheckClintParam(BaseModel):
    user: str = "root"
    password: str = "123123"
    host: List[str]


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
                list(vector_index_parameter.keys())[0]
            ].keys()
            for key, v in value.items():
                if key in index_keys:
                    vector_index_parameter[list(vector_index_parameter.keys())[0]][
                        key
                    ] = v
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
                else:
                    warnings.warn(f"index_config {key} not in {index_type}")

        vector_index_parameter[list(vector_index_parameter.keys())[0]][
            "dimension"
        ] = dimension
        vector_index_parameter[list(vector_index_parameter.keys())[0]][
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
    def check_true_positive_values(cls, value, field):
        if not value >= 0:
            raise ValueError(f"{field.name} must >= 0")
        return value

    @validator("start_id", "max_count", pre=True, always=True)
    def check_positive_values(cls, value, field):
        if not value > 0:
            raise ValueError(f"{field.name} must > 0")
        return value

    @validator(
        "is_reverse", "without_scalar_data", "without_table_data", pre=True, always=True
    )
    def check_boolean_fields(cls, value):
        return "true" if value else "false"

    @validator("without_vector_data", pre=True, always=True)
    def check_without_vector_data(cls, value):
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
                (key, {"fieldType": auto_value_type(value), "fields": [{"data": value}]})
                for key, value in value.items()
            )
            value = scalar_data
            return value


class CheckVectorSearchParam(BaseModel):
    index_name: str
    xq: list
    index_type: str
    top_k: int = 10
    pre_filter: bool = True
    brute:bool = False
    search_params: dict = None

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

    @validator("search_params", always=True)
    def check_search_params(cls, search_params, values):
        scalar_data = {}
        use_scalar_filter = "false"
        lanchain_json = None
        if search_params is not None:
            if "meta_expr" in search_params.keys() and "langchain_expr" in search_params.keys():
                raise ValueError(f"meta_expr and langchain_expr cannot coexist") 
            elif "meta_expr" in search_params.keys():
                if search_params["meta_expr"] is not None:
                    values["pre_filter"] = False
                    use_scalar_filter = "true"
                    scalar_data = dict(
                        (key, {"fieldType": auto_value_type(value), "fields": [{"data": value}]})
                        for key, value in search_params["meta_expr"].items()
                    )
                    
            elif "langchain_expr" in search_params.keys():
                if search_params["langchain_expr"] is not None:
                    values["pre_filter"] = True
                    lanchain_json = auto_expr_type(search_params["langchain_expr"])
            else:
                values["pre_filter"] = False
        else:
             values["pre_filter"] = False   

        ef_search = 32 if search_params is None else search_params.get("efSearch", 32)
        assert ef_search >= 0, f"efSearch must >= 0, but get {ef_search}"

        nprobe = 16 if search_params is None else search_params.get("nprobe", 16)
        assert nprobe >= 0, f"nprobe must >= 0, but get {nprobe}"
        recallNum = (
            100 if search_params is None else search_params.get("recallNum", 100)
        )
        assert recallNum > 0, f"recallNum must > 0, but get {recallNum}"
        index_type = values.get("index_type")

        with_Scalar_data = "false"
        with_vector_data = "false"
        if search_params is not None:
            if search_params.get("withScalarData") is not None:
                with_Scalar_data = search_params.get("withScalarData")
                with_Scalar_data = (
                    "false" if with_Scalar_data is None else with_Scalar_data
                )

            if search_params.get("withVectorData") is not None:
                with_vector_data = search_params.get("withVectorData")
                with_vector_data = (
                    "false" if with_vector_data is None else with_vector_data
                )
        parallel = (
            0 if search_params is None else search_params.get("parallelOnQueries", 0)
        )
        if index_type == "VECTOR_INDEX_TYPE_HNSW":
            search = {
                "hnswParam": {"efSearch": ef_search}
            }
        elif index_type == "VECTOR_INDEX_TYPE_FLAT":
            search = {
                "flat": {"parallelOnQueries": parallel}
            }
        elif index_type == "VECTOR_INDEX_TYPE_BRUTEFORCE":
            search = {}
        elif index_type == "VECTOR_INDEX_TYPE_IVF_FLAT":
            search = {
                "ivfFlatParam": {"nprobe": nprobe, "parallelOnQueries": parallel}
            }
        elif index_type == "VECTOR_INDEX_TYPE_IVF_PQ":
            search = {
                "ivfPqParam": {
                        "nprobe": nprobe,
                        "parallelOnQueries": parallel,
                        "recallNum": recallNum,
                    }
            }

        payload = {
            "parameter": {
                "useBruteForce": "true" if values.get("brute") else "false", 
                "search": search,
                "selectedKeys": [],
                "topN": values.get("top_k"),
                "withoutScalarData": with_Scalar_data,
                "withoutVectorData": with_vector_data,
                "useScalarFilter": use_scalar_filter,
                "vectorFilter": "SCALAR_FILTER",
                "vectorFilterType": "QUERY_PRE"
                if values.get("pre_filter")
                else "QUERY_POST",
            },
            "vectors": [
                {
                    "scalarData": scalar_data,
                    "vector": {
                        "binaryValues": [],
                        "dimension": len(xq),
                        "floatValues": xq,
                        "valueType": "FLOAT",
                    },
                }
                for xq in values.get("xq")
            ],
        }
        payload["parameter"].update({"langchainExpr": lanchain_json,
}) if lanchain_json is not None else ...
        return payload


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
