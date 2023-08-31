from dingodb.protos.proxy_common_pb2 import *
from dingodb.protos.proxy_index_pb2 import *
from dingodb.protos.proxy_index_pb2_grpc import *
from dingodb.protos.proxy_meta_pb2 import *
from dingodb.protos.proxy_meta_pb2_grpc import *
from google.protobuf.json_format import MessageToDict, ParseDict

import grpc
from grpc._cython import cygrpc

from .grpc_dingo_param import (
    CheckClintParam,
    CheckCreateIndexParam,
    CheckVectorAddParam,
    CheckVectorDeleteParam,
    CheckVectorGetParam,
    CheckVectorScanParam,
    CheckVectorSearchParam,
)


class GrpcDingoDB:
    def __init__(self, host: list, timeout: int = 55000) -> None:
        CheckClintParam(host=host, timeout=timeout)
        self._get_channel(host, timeout)
        self.index_stub = IndexServiceStub(self._channel)
        self.meta_stub = MetaServiceStub(self._channel)

    def _get_channel(self, host, timeout):
        self.opts = [
            (cygrpc.ChannelArgKey.max_send_message_length, -1),
            (cygrpc.ChannelArgKey.max_receive_message_length, -1),
            ("grpc.enable_retries", 1),
            ("grpc.keepalive_time_ms", timeout),
        ]
        # channel_list

        self._channel = grpc.insecure_channel(host[0], options=self.opts)

    def __del__(self):
        self._channel.close()

    def close(self):
        self._channel.close()

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

        describe_index_request = GetIndexRequest(
            schema_name="dingo", index_name=index_name
        )

        describe_index_response = self.meta_stub.GetIndex.future(describe_index_request)

        describe_info = MessageToDict(
            describe_index_response.result().definition,
            including_default_value_fields=True,
        )
        describe_info.update({"autoIncrement": int(describe_info["autoIncrement"])})

        return describe_info

    def describe_index_info_all(self) -> dict:
        """
        describe_index_info index info

        Raises:
            RuntimeError: return error

        Returns:
            List[dict]: index info
        """

        describe_indexes_request = GetIndexesRequest(schema_name="dingo")

        describe_indexes_response = self.meta_stub.GetIndexes.future(
            describe_indexes_request
        )
        return list(
            map(
                lambda definition: {
                    **MessageToDict(definition, including_default_value_fields=True),
                    "autoIncrement": int(
                        MessageToDict(definition, including_default_value_fields=True)[
                            "autoIncrement"
                        ]
                    ),
                },
                describe_indexes_response.result().definitions,
            )
        )

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
            index_type (str, optional): index type, one of {"flat", "hnsw"}. Defaults to "hnsw".
            metric_type (str, optional): metric type, one of {"dotproduct", "euclidean", "cosine"}. Defaults to "cosine"
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
        params = CheckCreateIndexParam(
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
        rule = PartitionRule(columns=[])
        if params.partition_rule == {} and operand is not None and len(operand) != 0:
            rule.func_name = "RANGE"
            for item in operand:
                rule.details.append(
                    PartitionDetailDefinition(
                        operand=[str(item)], operator="", part_name=""
                    )
                )
        vec_create_request = CreateIndexRequest(
            schema_name="dingo",
            definition=IndexDefinition(
                auto_increment=params.start_id if params.auto_id else 0,
                name=params.index_name,
                replica=params.replicas,
                version=0,
                with_auto_increment=params.auto_id,
                index_partition=rule,
                index_parameter=IndexParameter(
                    index_type=INDEX_TYPE_VECTOR,
                    vector_index_parameter=ParseDict(
                        params.index_config, VectorIndexParameter()
                    ),
                ),
            ),
        )
        vec_create_response = self.meta_stub.CreateIndex.future(vec_create_request)

        return vec_create_response.result().state

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

        update_index_max_element_request = UpdateMaxElementsRequest(
            schema_name="dingo", index_name=index_name, max_elements=max_element
        )

        update_index_max_element_response = self.meta_stub.UpdateMaxElements.future(
            update_index_max_element_request
        )

        return update_index_max_element_response.result().state

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
        # "name", "version", "index_partition", "replica", "index_parameter", "with_auto_increment", "auto_increment"
        update_index_request = UpdateIndexRequest(
            schema_name="dingo", definition=ParseDict(definition, IndexDefinition())
        )

        update_index_response = self.meta_stub.UpdateIndex.future(update_index_request)

        return update_index_response.result().state

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
        del_index_request = DeleteIndexRequest(
            schema_name="dingo", index_name=index_name
        )

        del_index_response = self.meta_stub.DeleteIndex.future(del_index_request)
        return del_index_response.result().state

    def vector_add(
        self, index_name: str, datas: list, vectors: list, ids: list = None
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
            list: add vector info in dingoDB
        """
        params = CheckVectorAddParam(
            index_name=index_name, datas=datas, vectors=vectors, ids=ids
        )

        vec_add_request = VectorAddRequest(
            schema_name="dingo", index_name=params.index_name
        )
        for i, v in enumerate(params.vectors):
            vec_grpc = VectorWithId()
            scalar_data_grpc = VectorScalarData()
            for key, value in params.datas[i].items():
                entry = scalar_data_grpc.scalar_data[key]
                entry.field_type = STRING
                field = entry.fields.add()
                field.string_data = value

            vec_grpc.vector.CopyFrom(
                Vector(dimension=len(v), float_values=v, value_type=FLOAT)
            )
            vec_grpc.scalar_data.CopyFrom(scalar_data_grpc)
            if ids is not None:
                vec_grpc.id = params.ids[i]
            vec_add_request.vectors.append(vec_grpc)

        vec_add_response = self.index_stub.VectorAdd.future(vec_add_request)

        return list(
            map(
                lambda vec: {
                    **MessageToDict(vec, including_default_value_fields=True),
                    "id": int(
                        MessageToDict(vec, including_default_value_fields=True)["id"]
                    ),
                    "scalarData": MessageToDict(
                        vec, including_default_value_fields=True
                    )["scalarData"]["scalarData"],
                }
                if MessageToDict(vec, including_default_value_fields=True)
                and int(MessageToDict(vec, including_default_value_fields=True)["id"])
                != 0
                else None,
                vec_add_response.result().vectors,
            )
        )

    def vector_count(self, index_name: str):
        """
        vector_count count in index

        Args:
            index_name (str): the name of in index

        Returns:
            int: count num
        """
        vec_count_request = VectorGetRegionMetricsRequest(
            schema_name="dingo", index_name=index_name
        )
        vec_count_response = self.index_stub.VectorGetRegionMetrics.future(
            vec_count_request
        )
        records = MessageToDict(vec_count_response.result().metrics)

        return int(records.get("currentCount", 0)) - int(records.get("deletedCount", 0))

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
        params = CheckVectorScanParam(
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

        vec_scan_request = VectorScanQueryRequest(
            schema_name="dingo",
            index_name=params.index_name,
            vector_id_end=params.end_id,
            max_scan_count=params.max_count,
            vector_id_start=params.start_id,
            is_reverse_scan=params.is_reverse,
            without_vector_data=not params.with_vector_data,
            with_scalar_data=params.with_scalar_data,
            with_table_data=params.with_table_data,
            selected_keys=params.fields,
        )
        if params.filter_scalar:
            scalar_data_grpc = VectorScalarData()
            for key, value in params.filter_scalar.items():
                entry = scalar_data_grpc.scalar_data[key]
                entry.field_type = STRING
                field = entry.fields.add()
                field.string_data = value
            vec_scan_request.use_scalar_filter = True
            vec_scan_request.scalar_for_filter.CopyFrom(scalar_data_grpc)
        vec_scan_response = self.index_stub.VectorScanQuery.future(vec_scan_request)

        return list(
            map(
                lambda vec: {
                    **MessageToDict(vec, including_default_value_fields=True),
                    "id": int(
                        MessageToDict(vec, including_default_value_fields=True)["id"]
                    ),
                    "scalarData": MessageToDict(
                        vec, including_default_value_fields=True
                    )["scalarData"]["scalarData"],
                },
                vec_scan_response.result().vectors,
            )
        )

    def get_index(self):
        """
        get_index get all index

        Raises:
            RuntimeError: return error

        Returns:
            list: all index list
        """

        get_index_name_request = GetIndexNamesRequest(schema_name="dingo")

        get_index_name_response = self.meta_stub.GetIndexNames.future(
            get_index_name_request
        )

        return get_index_name_response.result().names

    def get_max_index_row(self, index_name: str, get_min: bool = False):
        """
        get_max_index_row get max id in index

        Args:
            index_name (str): the name of in index
            get_min (bool): whether get min value


        Raises:
            RuntimeError: return error

        Returns:
            int: max id value
        """
        vec_max_id_request = VectorGetBorderIdRequest(
            schema_name="dingo", index_name=index_name, get_min=get_min
        )

        vec_max_id_response = self.index_stub.VectorGetBorderId.future(
            vec_max_id_request
        )

        return vec_max_id_response.result().id

    def vector_search(
        self,
        index_name: str,
        xq: list,
        top_k: int = 10,
        search_params: dict = None,
        pre_filter: bool = True,
    ) -> list:
        """
        vector_search search vector

        Args:
            index_name (str): the name of the index
            xq (list): query vector, List[float] or List[List[float]]
            top_k (int, optional): top k search. Defaults to 10.
            search_params (dict, optional): search params for index. Defaults to None.
            pre_filter (bool, optional): filter type for index, False is post-filter. Defaults to True.

        Raises:
            RuntimeError: return error

        Returns:
            List[dict]: search results
        """
        params = CheckVectorSearchParam(
            index_name=index_name,
            xq=xq,
            top_k=top_k,
            pre_filter=pre_filter,
            search_params=search_params,
        )

        vec_search_response = self.index_stub.VectorSearch.future(params.search_params)
        search_res = []
        for vec in vec_search_response.result().batch_results:
            res_info = []
            msg_dict = MessageToDict(vec, including_default_value_fields=True)
            for vec_info in msg_dict["vectorWithDistances"]:
                vec_info["vectorWithId"]["id"] = int(vec_info["vectorWithId"]["id"])
                vec_info["vectorWithId"]["scalarData"] = vec_info["vectorWithId"][
                    "scalarData"
                ]["scalarData"]
                vec_info.update(vec_info["vectorWithId"])
                vec_info.pop("vectorWithId")
                res_info.append(vec_info)
            msg_dict["vectorWithDistances"] = res_info
            search_res.append(msg_dict)

        return search_res

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
            RuntimeError: _description_

        Returns:
            list: _description_
        """
        params = CheckVectorGetParam(
            index_name=index_name, ids=ids, scalar=scalar, vector=vector
        )

        vec_get_request = VectorGetRequest(
            schema_name="dingo",
            index_name=params.index_name,
            vector_ids=params.ids,
            with_out_vector_data=not vector,
            with_scalar_data=scalar,
        )

        vec_get_response = self.index_stub.VectorGet.future(vec_get_request)

        # for vec in vec_get_response.result().vectors:
        #     print(MessageToDict(vec, including_default_value_fields=True))
        return list(
            map(
                lambda vec: {
                    **MessageToDict(vec, including_default_value_fields=True),
                    "id": int(
                        MessageToDict(vec, including_default_value_fields=True)["id"]
                    ),
                    "scalarData": MessageToDict(
                        vec, including_default_value_fields=True
                    )["scalarData"]["scalarData"],
                }
                if MessageToDict(vec, including_default_value_fields=True)
                and int(MessageToDict(vec, including_default_value_fields=True)["id"])
                != 0
                else None,
                vec_get_response.result().vectors,
            )
        )

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

        vec_del_request = VectorDeleteRequest(
            schema_name="dingo", index_name=params.index_name, ids=params.ids
        )

        vec_del_response = self.index_stub.VectorDelete.future(vec_del_request)
        return vec_del_response.result().key_states
