#!/usr/bin/python3
from .dingo_param import ClintParam, CreateIndexParam, VectorAddParam, VectorSearchParam, VectorGetParam, \
    VectorDeleteParam
from . import config
import requests
import json
import warnings


class DingoDB:
    headers = {"Content-Type": "application/json"}
    requestProto = "http://"
    indexApi = "/index/api/dingo/"
    vectorApi = "/vector/api/dingo/"
    
    def __init__(self, user, password, host) -> None:
        params = ClintParam(user=user, password=password, host=host)
        self.user = params.user
        self.password = params.password
        self.host = params.host

    def describe_index_info(self, index_name) -> dict:
        res = requests.get(f"{self.requestProto}{self.host[0]}{self.indexApi}{index_name}", headers=self.headers)
        if res.status_code == 200:
            return res.json()
        else:
            raise RuntimeError(res.json())

    def create_index(self,  index_name, dimension, index_type="hnsw", metric_type="euclidean", replicas=3,
                     index_config=None, metadata_config=None, partition_rule=None, auto_id=True) -> bool:

        params = CreateIndexParam(index_name=index_name, dimension=dimension, index_type=index_type,
                                  metric_type=metric_type, replicas=replicas, index_config=index_config,
                                  metadata_config=metadata_config, partition_rule=partition_rule, auto_id=auto_id)
        
        partition_rule = params.partition_rule if params.partition_rule is not None else {}
        
        if params.metric_type not in config.metric_type.keys():
            raise Exception(f"metric_type  must in {list(config.metric_type.keys())}")
        metric_type = config.metric_type[params.metric_type]

        if params.index_type not in config.index_config.keys():
            raise Exception(f"index_type  must in {list(config.index_config.keys())}")
        vector_index_parameter = config.index_config[params.index_type]

        if params.index_config is not None:
            for key, value in params.index_config:
                index_keys = vector_index_parameter[list(vector_index_parameter.keys())[0]].keys()
                if key in index_keys:
                    vector_index_parameter[list(vector_index_parameter.keys())[0]][key] = value
                    if key == "efConstruction" and key > 500 or key < 100:
                        warnings.warn(f"efConstruction: {key} suggestion in 100-500")
                    if key == "maxElements" and key > 10000000 or key < 50000:
                        warnings.warn(f"maxElements:{key} suggestion in 50000-10000000")
                    if key == "nlinks" and key > 64 or key < 16:
                        warnings.warn(f"nlinks:{key} suggestion in 16-64")
                else:
                    warnings.warn(f"index_config {key} not in {params.index_type}")
        
        vector_index_parameter[list(vector_index_parameter.keys())[0]]["dimension"] = params.dimension
        vector_index_parameter[list(vector_index_parameter.keys())[0]]["metricType"] = metric_type

        index_definition = {
            "autoIncrement": 1,
            "isAutoIncrement": "true" if auto_id else "false",
            "indexParameter": {
                "indexType": "INDEX_TYPE_VECTOR",
                "vectorIndexParameter": vector_index_parameter
            },
            "name": params.index_name,
            "partitionRule": partition_rule,
            "replica": params.replicas,
            "version": 0
        }
        # print(indexDefinition)
        res = requests.put(f"{self.requestProto}{self.host[0]}{self.indexApi}", headers=self.headers,
                           data=json.dumps(index_definition))
        if res.status_code == 200:
            return True
        raise RuntimeError(res.json())

    def delete_index(self, index_name) -> bool:
        res = requests.delete(f"{self.requestProto}{self.host[0]}{self.indexApi}{index_name}")
        if res.status_code == 200:
            return True
        raise RuntimeError(res.json())

    def vector_add(self, index_name, datas, vectors, ids=None) -> list:
        params = VectorAddParam(index_name=index_name, datas=datas, vectors=vectors, ids=ids)
        if ids is None:
            assert len(params.datas) == len(params.vectors), \
                f"length datas:{len(params.datas)} vectors: {len(params.vectors)} is not equal"
        else:
            assert len(params.datas) == len(params.vectors) == len(params.ids), \
                 f"length datas:{len(params.datas)} vectors: {len(params.vectors)} ids:{len(params.ids)} is not equal"

        records = []
        for i, v in enumerate(params.vectors):
            scalar_data = dict(
                    (key, {"fieldType": "STRING", "fields": [{"data": value}]})
                    for key, value in params.datas[i].items()
                )
            vector = {
                    "binaryValues": [],
                    "dimension": len(v),
                    "floatValues": v,
                    "valueType": "FLOAT"
            }
            record = {
                    "scalarData": scalar_data,
                    "vector": vector
                }
            if ids is not None:
                record.update({"id": params.ids[i]})
            
            records.append(record) 
            
        res = requests.put(f"{self.requestProto}{self.host[0]}{self.vectorApi}{params.index_name}",
                           headers=self.headers, data=json.dumps(records))
        if res.status_code == 200:
            records = res.json()
            return records
        raise RuntimeError(res.json())

    def get_index(self):
        res = requests.get(f"{self.requestProto}{self.host[0]}{self.indexApi}", headers=self.headers)
        if res.status_code == 200:
            indics = res.json()
            return indics
        raise RuntimeError(res.json())

    def get_max_index_row(self, index_name):
        payload = {"isGetMin": "false"}
        res = requests.get(f"{self.requestProto}{self.host[0]}{self.vectorApi}{index_name}/id", params=payload,
                           headers=self.headers)
        if res.status_code == 200:
            id = res.json()
            return id
        raise RuntimeError(res.json())

    def vector_search(self, index_name, xq, top_k=10, search_params=None) -> dict:
        params = VectorSearchParam(index_name=index_name, xq=xq, top_k=top_k, search_params=search_params)
        scalar_data = {}
        use_scalar_filter = "false"
        if params.search_params is not None and "meta_expr" in params.search_params.keys():
            use_scalar_filter = "true"
            scalar_data = dict(
                (key, {"fieldType": "STRING", "fields": [{"data": value}]})
                for key, value in params.search_params["meta_expr"].items()
            )
        
        payload = {
            "parameter": {
                "search": {
                    "hnswParam": {
                        "efSearch": 32 if search_params is None else search_params.get("efSearch", 32)
                        },
                    "flat":
                        {
                        "parallelOnQueries": 0 if search_params is None else search_params.get("parallelOnQueries", 0)
                        }
                    },
                "selectedKeys": [],
                "topN": params.top_k,
                "withScalarData": "true" if search_params is None else search_params.get("withScalarData", "true"),
                "withoutVectorData": "false" if search_params is None else search_params.get("withoutVectorData",
                                                                                             "false"),
                "useScalarFilter": use_scalar_filter
                },
            "vector": {
                "scalarData": scalar_data,
                "vector": {
                    "binaryValues": [],
                    "dimension": len(params.xq),
                    "floatValues": params.xq,
                    "valueType": "FLOAT"
                          }
                      }
               }
        res = requests.post(f"{self.requestProto}{self.host[0]}{self.vectorApi}{params.index_name}",
                            headers=self.headers, data=json.dumps(payload))
        if res.status_code == 200:
            records = res.json()
            return records
        raise RuntimeError(res.json())
    
    def vector_get(self, index_name, ids, scalar=True, vector=True) -> list:
        params = VectorGetParam(index_name=index_name, ids=ids, scalar=scalar, vector=vector)
        payload = {
            "ids": params.ids,
            "keys": [],
            "withScalarData": "true" if scalar else "false",
            "withoutVectorData": "false" if vector else "true"
        }
        res = requests.post(f"{self.requestProto}{self.host[0]}{self.vectorApi}{ params.index_name}/get",
                            headers=self.headers, data=json.dumps(payload))
        if res.status_code == 200:
            records = res.json()
            return records
        else:
            raise RuntimeError(res.json())

    def vector_delete(self, index_name, ids):
        params = VectorDeleteParam(index_name=index_name, ids=ids)
        res = requests.delete(f"{self.requestProto}{self.host[0]}{self.vectorApi}{params.index_name}",
                              headers=self.headers, data=json.dumps(params.ids))
        if res.status_code == 200:
            return res.json()
        else:
            raise RuntimeError(res.json())
