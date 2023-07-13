from pydantic import BaseModel
from typing import Any, Callable, Dict, List, Optional


class ClintParam(BaseModel):
    user: str = "root"
    password: str = "123123"
    host: List[str]


class CreateIndexParam(BaseModel):
    index_name: str
    dimension: int
    index_type: str = "hnsw"
    metric_type: str = "euclidean"
    replicas: int = 3
    index_config: dict = None
    metadata_config: dict = None
    partition_rule: dict = None
    auto_id: bool = True


class VectorAddParam(BaseModel):
    index_name: str
    datas: List[dict]
    vectors: List[list]
    ids: List[int] = None


class VectorSearchParam(BaseModel):
    index_name: str
    xq: list
    top_k: int = 10
    search_params: dict = None


class VectorGetParam(BaseModel):
    index_name: str
    ids: List[int]
    scalar: bool = True
    vector: bool = True


class VectorDeleteParam(BaseModel):
    index_name: str
    ids: List[int]
