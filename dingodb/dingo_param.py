from typing import List
import warnings

from pydantic import BaseModel, validator
from . import config


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
            index_keys = vector_index_parameter[list(vector_index_parameter.keys())[0]].keys()
            for key, v in value.items():
                if key in index_keys:
                    vector_index_parameter[list(vector_index_parameter.keys())[0]][key] = v
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
        
        vector_index_parameter[list(vector_index_parameter.keys())[0]]["dimension"] = dimension
        vector_index_parameter[list(vector_index_parameter.keys())[0]]["metricType"] = metric_type
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
            assert len(values.get("datas")) == len(values.get("vectors")), \
                f"length datas:{len(values.get('datas'))} vectors: {len(values.get('vectors'))} is not equal"
        else:
            assert len(values.get('datas')) == len(values.get('vectors')) == len(value), \
                f"length datas:{len(values.get('datas'))} vectors: {len(values.get('vectors'))} ids:{len(value)} is not equal"
        return value


class CheckVectorScanParam(BaseModel):
    index_name: str
    start_id: int
    max_count: int = 1000
    is_reverse: bool = False
    with_scalar_data: bool = True
    with_table_data: bool = True
    without_vector_data: bool = False
    fields: list = None
    
    @validator("*", always=True)
    def check_input(cls, value, field):
        if field.name == "start_id":
            if not value > 0:
                raise Exception("start_id must > 0")   
        if field.name == "max_count":
            if not value > 0:
                raise Exception("max_count must > 0")
        if field.name == "is_reverse" or field.name == "with_scalar_data" or field.name == "with_table_data" or \
                field.name == "without_vector_data":
            value = "true" if value else "false"
        if field.name == "fields":
            if value is None:
                value = []

        return value


class CheckVectorSearchParam(BaseModel):
    index_name: str
    xq: list
    top_k: int = 10
    search_params: dict = None

    @validator("xq", always=True)
    def check_xq(cls, value):
        if not isinstance(value[0], list):
            value = [value]
        return value
    
    @validator("search_params", always=True)
    def check_search_params(cls, search_params, values):
        scalar_data = {}
        use_scalar_filter = "false"
        if search_params is not None and "meta_expr" in search_params.keys():
            if search_params["meta_expr"] is not None:
                use_scalar_filter = "true"
                scalar_data = dict(
                    (key, {"fieldType": "STRING", "fields": [{"data": value}]})
                    for key, value in search_params["meta_expr"].items()
                )
        
        ef_search = 32 if search_params is None else search_params.get("efSearch", 32)
        assert ef_search >= 0, f"efSearch must >= 0, but get {ef_search}"

        payload = {
            "parameter": {
                "search": {
                    "hnswParam": {
                        "efSearch": ef_search
                        },
                    "flat":
                        {
                        "parallelOnQueries": 0 if search_params is None else search_params.get("parallelOnQueries", 0)
                        }
                    },
                "selectedKeys": [],
                "topN": values.get("top_k"),
                "withScalarData": "true" if search_params is None else search_params.get("withScalarData", "true"),
                "withoutVectorData": "false" if search_params is None else search_params.get("withoutVectorData",
                                                                                             "false"),
                "useScalarFilter": use_scalar_filter
                },
            "vectors": [{
                "scalarData": scalar_data,
                "vector": {
                    "binaryValues": [],
                    "dimension": len(xq),
                    "floatValues": xq,
                    "valueType": "FLOAT"
                            }
                        } for xq in values.get("xq")]
                }
        return payload


class CheckVectorGetParam(BaseModel):
    index_name: str
    ids: List[int]
    scalar: bool = True
    vector: bool = True


class CheckVectorDeleteParam(BaseModel):
    index_name: str
    ids: List[int]
