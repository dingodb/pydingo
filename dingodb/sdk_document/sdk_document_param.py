from pydantic import BaseModel, validator
from typing import List, Dict, Union


class CreateIndexParam(BaseModel):
    index_name: str
    replicas: int = 3
    operand: List[int] = None
    start_id: int = 0
    json_params: str = ""

    @validator("replicas", always=True)
    def check_replicas(cls, value):
        if value < 0:
            raise ValueError(f"{value} must >= 0")
        if value == 0:
            value = 3
        return value

    @validator("start_id", always=True)
    def check_start_id(cls, value):
        if value < 0:
            raise ValueError(f"{value} must >= 0")
        return value

    @validator("json_params", always=True)
    def check_json_params(cls, value):
        return value


class DocumentDeleteParam(BaseModel):
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
        assert len(id_list) > 0, f"ids list length must > 0, but get {id_list}"
        return id_list


class DocumentAddParam(BaseModel):
    index_name: str
    documents: List
    ids: List[int] = None

    @validator("documents", always=True)
    def check_documents(cls, value):
        return value

    @validator("ids", pre=True, always=True)
    def check_ids(cls, value, values):
        if value is not None:
            assert (
                    len(values.get("documents")) == len(value)
            ), f"length documents:{len(values.get('documents'))} ids:{len(value)} is not equal"
            for id in value:
                if id <= 0:
                    raise ValueError("id must > 0")
        return value


class DocumentSearchParam(BaseModel):
    index_name: str
    query_string: str
    top_n: int = 0
    use_id_filter: bool = False
    doc_ids: List[int] = None
    with_scalar_data: bool = False
    column_names: List[str] = None
    selected_keys: List[str] = None
    query_limit: int = 40960

    @validator("top_n", pre=True, always=True)
    def check_top_k(cls, value, field):
        if not value > 0:
            raise ValueError(f"{field.name} must > 0")
        return value

    @validator("doc_ids", always=True)
    def check_doc_ids(cls, value, values):
        if value is None or value == []:
            value = []
            return value
        else:
            values["use_id_filter"] = True
            return value

    @validator("column_names", always=True)
    def check_column_names(cls, value):
        if value is None:
            value = []
        return value

    @validator("selected_keys", always=True)
    def check_selected_keys(cls, value):
        if value is None:
            value = []
        return value
    
    @validator("query_limit", always=True)
    def check_query_limit(cls, value):
        if value < 0 or value > 40960:
            raise ValueError(f"{value} must >= 0 and < 40960")
        return value


class DocumentQueryParam(BaseModel):
    index_name: str
    doc_ids: List[int]
    with_scalar_data: bool = False
    selected_keys: List[str] = None
    
    @validator("doc_ids", always=True)
    def check_doc_ids(cls, value):
        id_list = []
        for id in value:
            if id <= 0:
                raise Exception("id must > 0")
            else:
                id_list.append(id)
        assert len(id_list) > 0, f"doc_ids list length must > 0, but get {id_list}"
        return id_list

    @validator("selected_keys", always=True)
    def check_selected_keys(cls, value):
        if value is None:
            value = []
        return value


class DocumentGetBorderParam(BaseModel):
    index_name: str
    is_max: bool = True


class DocumentScanQueryParam(BaseModel):
    index_name: str
    doc_id_start: int
    doc_id_end: int = 0
    is_reverse: bool = False
    max_scan_count: int = 0
    with_scalar_data: bool = True
    selected_keys: List[str] = None

    @validator("is_reverse", always=True)
    def check_is_reverse(cls, value, values):
        if value:
            if values.get("doc_id_start") <= values.get("doc_id_end"):
                raise ValueError("doc_id_end must be less than doc_id_start in reverse scan")
        elif not value:
            if values.get("doc_id_start") >= values.get("doc_id_end") and values.get("doc_id_end") != 0:
                raise ValueError("doc_id_end must be greater than doc_id_start in forward scan")
        return value

    @validator("selected_keys", always=True)
    def check_selected_keys(cls, value):
        if value is None:
            value = []
        return value


class DocumentCountParam(BaseModel):
    index_name: str
    doc_id_start: int
    doc_id_end: int

    @validator("doc_id_end", always=True)
    def check_doc_id_end(cls, value, values):
        if value <= values.get("doc_id_start"):
            raise ValueError(f"doc_id_end must > doc_id_start")
        return value