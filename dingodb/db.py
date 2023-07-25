#!/usr/bin/python3
import json
import requests

from .dingo_param import CheckClintParam, CheckCreateIndexParam, CheckVectorAddParam, CheckVectorSearchParam, \
    CheckVectorGetParam, CheckVectorDeleteParam, CheckVectorScanParam


class DingoDB:
    headers = {"Content-Type": "application/json"}
    requestProto = "http://"
    indexApi = "/index/api/dingo/"
    vectorApi = "/vector/api/dingo/"
    
    def __init__(self, user: str, password: str, host: list) -> None:
        """
        __init__ init DingoDB

        Args:
            user (str): DingoDB user
            password (str): DingoDB password
            host (list): DingoDB host:port
        """
        params = CheckClintParam(user=user, password=password, host=host)
        self.user = params.user
        self.password = params.password
        self.host = params.host
        self.session = requests.Session()
    
    def __del__(self):
        self.session.close()
        
    def close(self):
        self.session.close()

    def describe_index_info(self, index_name: str) -> dict:
        """
        describe_index_info index info

        Args:
            index_name (str): the name the index

        Raises:
            RuntimeError: return error

        Returns:
            dict: index info
        """
        res = self.session.get(f"{self.requestProto}{self.host[0]}{self.indexApi}{index_name}", headers=self.headers)
        
        if res.status_code == 200:
            return res.json()
        else:
            raise RuntimeError(res.json())

    def create_index(self,  index_name: str, dimension: int, index_type: str = "hnsw", metric_type: str = "euclidean",
                     replicas: int = 3, index_config: dict = None, metadata_config: dict = None,
                     partition_rule: dict = None, operand: list = None, auto_id: bool = True,
                     start_id: int = 1) -> bool:
        """
        create_index create index

        Args:
            index_name (str): the name of index
            dimension (int): dimension of vector
            index_type (str, optional): index type, one of {"flat", "hnsw"}. Defaults to "hnsw".
            metric_type (str, optional): metric type, one of {"dotproduct", "euclidean"}. Defaults to "euclidean".
            replicas (int, optional): dingoDB store replicas. Defaults to 3.
            index_config (dict, optional): Advanced configuration options for the index. Defaults to None.
            metadata_config (dict, optional): metadata. Defaults to None.
            partition_rule (dict, optional): partition rule. Defaults to None.
            operand (list, optional): operand. Defaults to None.
            auto_id (bool, optional): isAutoIncrement or not isAutoIncrement. Defaults to True.
            start_id (int, optional): autoIncrement start id. Defaults to 1.

        Raises:
            RuntimeError: return error

        Returns:
            bool: create table status
        """
        params = CheckCreateIndexParam(index_name=index_name, dimension=dimension, index_type=index_type,
                                       metric_type=metric_type, replicas=replicas, index_config=index_config,
                                       metadata_config=metadata_config, partition_rule=partition_rule, operand=operand,
                                       auto_id=auto_id, start_id=start_id)

        if params.partition_rule == {} and operand is not None and len(operand) != 0:
            details = []
            for item in operand:
                details.append(
                    {
                        "operand": [item],
                        "operator": "",
                        "partName": ""
                    }
                )
            partition_rule = {
                "cols": [],
                "details": details,
                "funcName": ""
            }

        index_definition = {
            "autoIncrement": params.start_id,
            "isAutoIncrement": "true" if params.auto_id else "false",
            "indexParameter": {
                "indexType": "INDEX_TYPE_VECTOR",
                "vectorIndexParameter": params.index_config
            },
            "name": params.index_name,
            "indexPartition": partition_rule if partition_rule is not None else params.partition_rule,
            "replica": params.replicas,
            "version": 0
        }
        res = self.session.post(f"{self.requestProto}{self.host[0]}{self.indexApi}", headers=self.headers,
                                data=json.dumps(index_definition))
        if res.status_code == 200:
            return True
        else:
            raise RuntimeError(res.json())

    def update_index_max_element(self, index_name: str, max_element: int) -> bool:
        """
        update_index_max_element change index max element

        only for hnsw

        Args:
            index_name (str): the name of index
            max_element (int): max element value

        Raises:
            RuntimeError: return error

        Returns:
            bool: True/False
        """
        
        res = self.session.put(f"{self.requestProto}{self.host[0]}{self.indexApi}{index_name}/{max_element}")
        if res.status_code == 200:
            return True
        else:
            raise RuntimeError(res.json())
    
    def delete_index(self, index_name: str) -> bool:
        """
        delete_index del/drop index

        Args:
            index_name (str): the name of index

        Raises:
            RuntimeError: return error

        Returns:
            bool: True/False
        """
        res = self.session.delete(f"{self.requestProto}{self.host[0]}{self.indexApi}{index_name}")
        if res.status_code == 200:
            return True
        else:
            raise RuntimeError(res.json())

    def vector_add(self, index_name: str, datas: list, vectors: list, ids: list = None) -> list:
        """
        vector_add add vector

        Args:
            index_name (str): the name of index
            datas (list): metadata list 
            vectors (list): vector list
            ids (list, optional): id list. Defaults to None.

        Raises:
            RuntimeError: return error

        Returns:
            list: add vector info in dingoDB
        """
        params = CheckVectorAddParam(index_name=index_name, datas=datas, vectors=vectors, ids=ids)

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
        res = self.session.put(f"{self.requestProto}{self.host[0]}{self.vectorApi}{params.index_name}",
                               headers=self.headers, data=json.dumps(records))
        if res.status_code == 200:
            records = res.json()
            return records
        else:
            raise RuntimeError(res.json())
    
    def vector_count(self, index_name: str):
        """
        vector_count count in index

        Args:
            index_name (str): the name of in index
        
        Returns:
            int: count num
        """
        res = self.session.get(f"{self.requestProto}{self.host[0]}{self.vectorApi}{index_name}", headers=self.headers)
        if res.status_code == 200:
            records = res.json()
            return records.get("currentCount") - records.get("deletedCount")
        else:
            raise RuntimeError(res.json())
        
    def vector_scan(self, index_name: str, start_id: int, max_count: int = 1000, is_reverse: bool = False,
                    with_scalar_data: bool = True, with_table_data: bool = True, without_vector_data: bool = False,
                    filter_scalar: list = None) -> list:
        """
        vector_scan scan with start_id

        Args:
            index_name (str): the name of in index
            start_id (int): start id
            max_count (int, optional): max scan count. Defaults to 1000.
            is_reverse (bool, optional): whether or not reverse. Defaults to False.
            with_scalar_data (bool, optional): whether  with scalar info. Defaults to True.
            with_table_data (bool, optional): whether  with table info. Defaults to True.
            without_vector_data (bool, optional): whether with vector info. Defaults to False.
            filter_scalar (list, optional): scalar filter filed. Defaults to [].

        Raises:
            RuntimeError: return error

        Returns:
            list:  scan info list
        """
        params = CheckVectorScanParam(index_name=index_name, start_id=start_id, max_count=max_count,
                                      is_reverse=is_reverse, with_scalar_data=with_scalar_data,
                                      with_table_data=with_table_data, without_vector_data=without_vector_data,
                                      filter_scalar=filter_scalar)
        payload = {
            "isReverseScan": params.is_reverse,
            "maxScanCount": params.max_count,
            "selectedKeys": params.filter_scalar,
            "startId": params.start_id,
            "withScalarData": params.with_scalar_data,
            "withTableData": params.with_table_data,
            "withoutVectorData": params.without_vector_data
        }
        res = self.session.post(f"{self.requestProto}{self.host[0]}{self.vectorApi}{params.index_name}/scan",
                                headers=self.headers, data=json.dumps(payload))
        if res.status_code == 200:
            records = res.json()
            return records
        else:
            raise RuntimeError(res.json())
        
    def get_index(self):
        """
        get_index get all index

        Raises:
            RuntimeError: return error

        Returns:
            list: all index list 
        """

        res = self.session.get(f"{self.requestProto}{self.host[0]}{self.indexApi}", headers=self.headers)
        if res.status_code == 200:
            indics = res.json()
            return indics
        else:
            raise RuntimeError(res.json())

    def get_max_index_row(self, index_name: str):
        """
        get_max_index_row get max id in index

        Args:
            index_name (str): the name of in index 

        Raises:
            RuntimeError: return error

        Returns:
            int: max id value
        """
        payload = {"isGetMin": "false"}

        res = self.session.get(f"{self.requestProto}{self.host[0]}{self.vectorApi}{index_name}/id",
                               params=payload, headers=self.headers)
        if res.status_code == 200:
            max_id = res.json()
            return max_id
        else:
            raise RuntimeError(res.json())

    def vector_search(self, index_name: str, xq: list, top_k: int = 10, search_params: dict = None) -> dict:
        """
        vector_search search vector

        Args:
            index_name (str): the name of the index 
            xq (list): query vector, List[float] or List[List[float]]
            top_k (int, optional): top k search. Defaults to 10.
            search_params (dict, optional): search params for index. Defaults to None.

        Raises:
            RuntimeError: return error

        Returns:
            List[dict]: search results
        """
        params = CheckVectorSearchParam(index_name=index_name, xq=xq, top_k=top_k, search_params=search_params)
        
        res = self.session.post(f"{self.requestProto}{self.host[0]}{self.vectorApi}{params.index_name}",
                                headers=self.headers, data=json.dumps(params.search_params))
        
        if res.status_code == 200:
            records = res.json()
            return records
        else:
            raise RuntimeError(res.json())
    
    def vector_get(self, index_name: str, ids: list, scalar: bool = True, vector: bool = True) -> list:
        """
        vector_get query vector

        Args:
            index_name (str): the name of the index
            ids (list): query id list 
            scalar (bool, optional): res with or without scalar. Defaults to True.
            vector (bool, optional): res with or without vector. Defaults to True.

        Raises:
            RuntimeError: _description_

        Returns:
            list: _description_
        """
        params = CheckVectorGetParam(index_name=index_name, ids=ids, scalar=scalar, vector=vector)
        payload = {
            "ids": params.ids,
            "keys": [],
            "withScalarData": "true" if scalar else "false",
            "withoutVectorData": "false" if vector else "true"
        }
        
        res = self.session.post(f"{self.requestProto}{self.host[0]}{self.vectorApi}{params.index_name}/get",
                                headers=self.headers, data=json.dumps(payload))
        
        if res.status_code == 200:
            records = res.json()
            return records
        else:
            raise RuntimeError(res.json())

    def vector_delete(self, index_name: str, ids: list):
        """
        vector_delete delete vector with ids

        Args:
            index_name (str): the name of the index
            ids (list): id list 

        Raises:
            RuntimeError: return error

        Returns:
            list : [True, False, ...]
        """
        params = CheckVectorDeleteParam(index_name=index_name, ids=ids)
        
        res = self.session.delete(f"{self.requestProto}{self.host[0]}{self.vectorApi}{params.index_name}",
                                  headers=self.headers, data=json.dumps(params.ids))
        
        if res.status_code == 200:
            return res.json()
        else:
            raise RuntimeError(res.json())
