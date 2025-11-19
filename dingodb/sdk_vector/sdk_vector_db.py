#!/usr/bin/python3

from dingodb.sdk_client import SDKClient
from dingodb.sdk_vector.sdk_vector_client import SDKVectorClient

from dingodb.common.vector_rep import ScalarSchema, RegionState, RegionStatus
from dingodb.common.document_rep import DocumentSchema
from typing import  Optional

from .sdk_vector_param import (
    CreateIndexParam,
    VectorAddParam,
    VectorScanParam,
    VectorSearchParam,
    VectorGetParam,
    VectorDeleteParam,
    VectorStatusByRegionIdParam,
    VectorBuildByRegionIdParam,
    VectorLoadByRegionIdParam,
    VectorResetByRegionIdParam,
)


class SDKVectorDingoDB:
    def __init__(self, client: SDKClient):
        """
        __init__ init DingoSDK

        Args:
            client: SDKClient
        """
        self.client = SDKVectorClient(client)

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
        raise RuntimeError("not implement")

    def describe_index_info_all(self) -> dict:
        """
        describe_index_info index info

        Raises:
            RuntimeError: return error

        Returns:
            List[dict]: index info
        """
        raise RuntimeError("not implement")

    def create_index(
        self,
        index_name: str,
        dimension: int,
        index_type: str = "hnsw",
        metric_type: str = "cosine",
        replicas: int = 3,
        index_config: dict = None,
        metadata_config: dict = None,
        partition_rule: dict = None,
        operand: list = None,
        auto_id: bool = True,
        start_id: int = 1,
    ) -> bool:
        """
        create_index create index

        Args:
            index_name (str): the name of index
            dimension (int): dimension of vector
            index_type (str, optional): index type, one of {"flat", "hnsw","ivf_flat", "ivf_pq", "brute"}. Defaults to "hnsw".
            metric_type (str, optional): metric type, one of {"dotproduct", "euclidean", "cosine"}. Defaults to "cosine"
            replicas (int, optional): dingoDB store replicas. Defaults to 3.
            index_config (dict, optional): Advanced configuration options for the index. Defaults to None.
            metadata_config (dict, optional): metadata. Defaults to None.NOT Support Now , used for schema
            partition_rule (dict, optional): partition rule. Defaults to None. NOT Support Now
            operand (list, optional): operand. Defaults to None.
            auto_id (bool, optional): isAutoIncrement or not isAutoIncrement. Defaults to True.
            start_id (int, optional): autoIncrement start id. Defaults to 1.

        Raises:
            RuntimeError: return error

        Returns:
            bool: create table status
        """
        params = CreateIndexParam(
            index_name=index_name,
            dimension=dimension,
            index_type=index_type,
            metric_type=metric_type,
            replicas=replicas,
            index_config=index_config,
            metadata_config=metadata_config,
            partition_rule=partition_rule,
            operand=operand,
            auto_id=auto_id,
            start_id=start_id,
        )

        return self.client.create_index(params)

    def create_index_with_schema(
        self,
        index_name: str,
        dimension: int,
        schema: ScalarSchema,
        index_type: str = "hnsw",
        metric_type: str = "cosine",
        replicas: int = 3,
        index_config: dict = None,
        metadata_config: dict = None,
        partition_rule: dict = None,
        operand: list = None,
        auto_id: bool = True,
        start_id: int = 1,
        enable_scalar_speed_up_with_document: bool = False,
        json_params: Optional[str] = None,
        document_schema: DocumentSchema = None,
    ) -> bool:
        """
        create_index create index

        Args:
            index_name (str): the name of index
            dimension (int): dimension of vector
            schema (ScalarSchema): schema of scalar
            index_type (str, optional): index type, one of {"flat", "hnsw","ivf_flat", "ivf_pq", "brute","binary_flat","binary_ivf_flat"}. Defaults to "hnsw".
            metric_type (str, optional): metric type, one of {"dotproduct", "euclidean", "cosine","hamming"}. Defaults to "cosine"
            replicas (int, optional): dingoDB store replicas. Defaults to 3.
            index_config (dict, optional): Advanced configuration options for the index. Defaults to None.
            metadata_config (dict, optional): metadata. Defaults to None.NOT Support Now , used for schema
            partition_rule (dict, optional): partition rule. Defaults to None. NOT Support Now
            operand (list, optional): operand. Defaults to None.
            auto_id (bool, optional): isAutoIncrement or not isAutoIncrement. Defaults to True.
            start_id (int, optional): autoIncrement start id. Defaults to 1.
            enable_scalar_speed_up_with_document (bool, optional) enable_scalar_speed_up_with_document Defaults false
            json_params(str, optional) json_params for scalar_speed_up_with_document
            document_schema (ScalarSchema): document_schema of scalar

        Raises:
            RuntimeError: return error

        Returns:
            bool: create table status
        """
        params = CreateIndexParam(
            index_name=index_name,
            dimension=dimension,
            index_type=index_type,
            metric_type=metric_type,
            replicas=replicas,
            index_config=index_config,
            metadata_config=metadata_config,
            partition_rule=partition_rule,
            operand=operand,
            auto_id=auto_id,
            start_id=start_id,
            enable_scalar_speed_up_with_document=enable_scalar_speed_up_with_document,
            json_params=json_params,
        )

        return self.client.create_index(param=params, schema=schema,document_schema=document_schema)

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
        return True

    def update_index(self, index_name: str, definition: dict) -> bool:
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
        return True

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
        return self.client.delete_index(index_name)

    # TODO: only return vector ids
    def vector_add(
        self, index_name: str, datas: list, vectors: list, ids: list = None,value_type: str="float"
    ) -> list:
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
            list: vector id list
        """
        params = VectorAddParam(
            index_name=index_name, datas=datas, vectors=vectors, ids=ids,value_type=value_type
        )

        return self.client.vector_add(params)

    def vector_upsert(
        self, index_name: str, datas: list, vectors: list, ids: list = None ,value_type: str="float"
    ) -> list:
        """
        vector_upsert upsert vector

        Args:
            index_name (str): the name of index
            datas (list): metadata list
            vectors (list): vector list
            ids (list, optional): id list. Defaults to None.

        Raises:
            RuntimeError: return error

        Returns:
            list: upsert vector info in dingoDB
        """
        params = VectorAddParam(
            index_name=index_name, datas=datas, vectors=vectors, ids=ids,value_type=value_type
        )

        return self.client.vector_upsert(params)

    def vector_count(self, index_name: str):
        """
        vector_count count in index

        Args:
            index_name (str): the name of in index

        Raises:
            RuntimeError: return error

        Returns:
            int: count num
        """
        return self.client.vector_count(index_name)

    def vector_metrics(self, index_name: str):
        """
        vector_metrics metrics in index

        Args:
            index_name (str): the name of in index

        Returns:
            str: metrics string
        """
        return self.client.vector_metrics(index_name)

    def vector_scan(
        self,
        index_name: str,
        start_id: int,
        max_count: int = 1000,
        is_reverse: bool = False,
        with_scalar_data: bool = True,
        with_table_data: bool = True,
        with_vector_data: bool = True,
        fields: list = None,
        filter_scalar: dict = None,
        end_id: int = 0,
    ) -> list:
        """
        vector_scan scan with start_id

        Args:
            index_name (str): the name of in index
            start_id (int): start id
            max_count (int, optional): max scan count. Defaults to 1000.
            is_reverse (bool, optional): whether reverse. Defaults to False.
            with_scalar_data (bool, optional): whether  with scalar info. Defaults to True.
            with_table_data (bool, optional): whether  with table info. Defaults to True.
            with_vector_data (bool, optional): whether with vector info. Defaults to True.
            fields (list, optional): fields for return . Defaults to [].
            filter_scalar (dict, optional): filter_scalar for return . Defaults to None.
            end_id (int, optional): if end_id=0, get all max_count . Defaults to 0.

        Raises:
            RuntimeError: return error

        Returns:
            list:  scan info list
        """
        params = VectorScanParam(
            index_name=index_name,
            start_id=start_id,
            max_count=max_count,
            is_reverse=is_reverse,
            with_scalar_data=with_scalar_data,
            with_table_data=with_table_data,
            with_vector_data=with_vector_data,
            fields=fields,
            filter_scalar=filter_scalar,
            end_id=end_id,
        )

        return self.client.vector_scan(params)

    def get_index(self):
        """
        get_index get all index

        Raises:
            RuntimeError: return error

        Returns:
            list: all index list
        """
        return []

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
        return self.client.get_max_index_row(index_name=index_name)

    def vector_search(
        self,
        index_name: str,
        xq: list,
        top_k: int = 10,
        search_params: dict = None,
        pre_filter: bool = True,
        brute: bool = False,
        value_type: str = "float",
        is_scalar_speed_up_with_document: bool = False,
        query_string: str = ""
    ) -> list:
        """
        vector_search search vector

        Args:
            index_name (str): the name of the index
            xq (list): query vector, List[float] or List[List[float]]
            top_k (int, optional): top k search. Defaults to 10.
            search_params (dict, optional): search params for index. Defaults to None.
            pre_filter (bool, optional): filter type for index, False is post-filter. Defaults to True.
            brute (bool, optional): whether to turn on brute force search. Defaults to True.
            is_scalar_speed_up_with_document(bool, optional)):Whether to use scalar_speed_up_with_document, Default 

        Raises:
            RuntimeError: return error

        Returns:
            List[dict]: search results
        """

        params = VectorSearchParam(
            index_name=index_name,
            xq=xq,
            top_k=top_k,
            pre_filter=pre_filter,
            is_scalar_speed_up_with_document=is_scalar_speed_up_with_document,
            search_params=search_params,
            brute=brute,
            value_type=value_type,
            query_string=query_string
        )

        return self.client.vector_search(params)

    def vector_get(
        self, index_name: str, ids: list, scalar: bool = True, vector: bool = True
    ) -> list:
        """
        vector_get query vector

        Args:
            index_name (str): the name of the index
            ids (list): query id list
            scalar (bool, optional): res with or without scalar. Defaults to True.
            vector (bool, optional): res with or without vector. Defaults to True.

        Raises:
            RuntimeError

        Returns:
            list: VectorWithId dict
        """
        params = VectorGetParam(
            index_name=index_name,
            ids=ids,
            with_scalar_data=scalar,
            with_vector_data=vector,
        )

        return self.client.vector_get(params)

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
        params = VectorDeleteParam(index_name=index_name, ids=ids)

        return self.client.vector_delete(params)

    def vector_status_by_index(self, index_name: str) -> list[RegionState]:
        """
        vector_status_by_index

        Args:
            index_name: str

        Raises:
            RuntimeError: return error

        Returns:
            list: state list
        """
        return self.client.vector_status_by_index(index_name=index_name)

    def vector_status_by_region(self, index_name: str, ids: list) -> list[RegionState]:
        """
        vector_status_by_region

        Args:
             index_name: str
              ids: list

        Raises:
            RuntimeError: return error

        Returns:
            list: state list
        """
        params = VectorStatusByRegionIdParam(index_name=index_name, ids=ids)
        return self.client.vector_status_by_region(params)

    def vector_build_by_index(self, index_name: str) -> list[RegionStatus]:
        """
        vector_build_by_index

        Args:
            index_name: str

        Raises:
            RuntimeError: return error

        Returns:
            list: err_status list
        """
        return self.client.vector_build_by_index(index_name=index_name)

    def vector_build_by_region(self, index_name: str, ids: list) -> list[RegionStatus]:
        """
        vector_build_by_index

        Args:
           index_name: str
            ids: list

        Raises:
            RuntimeError: return error

        Returns:
            list: err_status list
        """
        params = VectorBuildByRegionIdParam(index_name=index_name, ids=ids)
        return self.client.vector_build_by_region(params)

    def vector_load_by_index(self, index_name: str) -> list[RegionStatus]:
        """
        vector_load_by_index

        Args:
            index_name: str

        Raises:
            RuntimeError: return error

        Returns:
            list: err_status list
        """
        return self.client.vector_load_by_index(index_name=index_name)

    def vector_load_by_region(self, index_name: str, ids: list) -> list[RegionStatus]:
        """
        vector_load_by_region

        Args:
            index_name: str
             ids: list

        Raises:
            RuntimeError: return error

        Returns:
            list: err_status list
        """
        params = VectorLoadByRegionIdParam(index_name=index_name, ids=ids)
        return self.client.vector_load_by_region(params)

    def vector_reset_by_index(self, index_name: str) -> list[RegionStatus]:
        """
        vector_reset_by_index

        Args:
            index_name: str

        Raises:
            RuntimeError: return error

        Returns:
            list: err_status list
        """
        return self.client.vector_reset_by_index(index_name=index_name)

    def vector_reset_by_region(self, index_name: str, ids: list) -> list[RegionStatus]:
        """
        vector_reset_by_region

        Args:
            index_name: str
             ids: list

        Raises:
            RuntimeError: return error

        Returns:
            list: err_status list
        """
        params = VectorResetByRegionIdParam(index_name=index_name, ids=ids)
        return self.client.vector_reset_by_region(params)

    def vector_import_add(
        self, index_name: str, datas: list, vectors: list, ids: list = None
    ) -> list:
        """
        vector_import_add add vector

        Args:
            index_name (str): the name of index
            datas (list): metadata list
            vectors (list): vector list
            ids (list, optional): id list. Defaults to None.

        Raises:
            RuntimeError: return error

        Returns:
            list: vector id list
        """
        params = VectorAddParam(
            index_name=index_name, datas=datas, vectors=vectors, ids=ids
        )

        return self.client.vector_import_add(params)

    def vector_import_delete(self, index_name: str, ids: list):
        """
        vector_delete delete vector with ids

        Args:
            index_name (str): the name of the index
            ids (list): id list

        Raises:
            RuntimeError: return error

        Returns:

        """
        params = VectorDeleteParam(index_name=index_name, ids=ids)

        return self.client.vector_import_delete(params)

    def vector_count_memory(self, index_name: str) -> int:
        """
        vector_count_memory  count build vectors

        Args:
           index_name: str

        Raises:
            RuntimeError: return error

        Returns:
            count
        """
        return self.client.vector_count_memory(index_name=index_name)

    def vector_get_auto_increment_id(self, index_name: str) -> int:
        """
        vector_get_auto_increment_id get_auto_increment_id

        Args:
           index_name: str

        Raises:
            RuntimeError: return error

        Returns:
            auto_increment_id
        """
        return self.client.vector_get_auto_increment_memory(index_name=index_name)

    def vector_update_auto_increment_id(self, index_name: str, start_id: int):
        """
        vector_update_auto_increment_id update AutoIncrementId

        Args:
           index_name: str

        Raises:
            RuntimeError: return error

        Returns:

        """
        return self.client.vector_update_auto_increment_id(
            index_name=index_name, start_id=start_id
        )
    
    def vector_dump(self, index_name: str)-> list:
        return self.client.vector_dump(index_name=index_name)
