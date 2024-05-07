#!/usr/bin/python3

import json
import dingosdk
from dingodb.utils.tools import auto_value_type
from dingodb.common import constants
from dingodb.utils.tools import auto_value_type, auto_expr_type, convert_dict_to_expr

from .sdk_param import (
    CreateIndexParam,
    VectorAddParam,
    VectorScanParam,
    VectorSearchParam,
    VectorGetParam,
    VectorDeleteParam,
)

from .sdk_param_factory import SDKParamFactory
from .sdk_adapter import (
    sdk_search_result_to_search_result,
    sdk_vector_with_id_to_vector_with_id,
)

sdk_types = {
    "STRING": dingosdk.kSTRING,
    "DOUBLE": dingosdk.kDOUBLE,
    "INT64": dingosdk.kINT64,
    "BOOL": dingosdk.kBOOL,
}


class SDKClient:
    def __init__(self, coor_url: str):
        """
        __init__ init Client

        Args:
            coor_url (str): coordinator url, try to use like file://./coor_list
        """
        self.schema_id = 2
        s, self.client = dingosdk.Client.Build(coor_url)
        if not s.ok():
            raise RuntimeError(f"dongo client build fail: {s.ToString()}")
        s, self.vector_client = self.client.NewVectorClient()
        if not s.ok():
            raise RuntimeError(f"dongo vector client build fail: {s.ToString()}")

    def create_index(self, param: CreateIndexParam) -> bool:
        """
        create_index create index

        Args:
            param (CreateIndexParam): create index param

        Returns:
            bool: create index result
        """
        s, creator = self.client.NewVectorIndexCreator()
        assert s.ok(), f"dingo creator build fail: {s.ToString()}"
        creator.SetSchemaId(self.schema_id)
        creator.SetName(param.index_name)
        creator.SetReplicaNum(param.replicas)
        if not param.operand:
            creator.SetRangePartitions(param.operand)

        index_type = param.index_type
        if index_type == "flat":
            sdk_param = SDKParamFactory.create_flat_param(
                index_type, param.index_config
            )
            creator.SetFlatParam(sdk_param)
        elif index_type == "ivf_flat":
            sdk_param = SDKParamFactory.create_ivf_flat_param(
                index_type, param.index_config
            )
            creator.SetIvfFlatParam(sdk_param)
        elif index_type == "ivf_pq":
            sdk_param = SDKParamFactory.create_ivf_pq_param(
                index_type, param.index_config
            )
            creator.SetIvfPqParam(sdk_param)
        elif index_type == "hnsw":
            sdk_param = SDKParamFactory.create_hnsw_param(
                index_type, param.index_config
            )
            creator.SetHnswParam(sdk_param)
        elif index_type == "brute":
            sdk_param = SDKParamFactory.create_brute_param(
                index_type, param.index_config
            )
            creator.SetBruteForceParam(sdk_param)
        else:
            raise RuntimeError(f"index_type: {index_type} not support")

        if param.auto_id:
            creator.SetAutoIncrementStart(param.start_id)

        index_id = -1
        s, index_id = creator.Create()
        if s.ok():
            return True
        else:
            raise RuntimeError(
                f"create index {param.index_name} fail: {s.ToString()}, index_id: {index_id}"
            )

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
        s = self.client.DropIndexByName(self.schema_id, index_name)
        if s.ok():
            return True
        else:
            raise RuntimeError(f"delete index {index_name} fail: {s.ToString()}")

    def vector_add(self, add_param: VectorAddParam) -> list:
        """
        vector_add add vector

        Args:
            add_param: VectorAddParam

        Raises:
            RuntimeError: return error

        Returns:
            list: vector id list
        """
        vectors = dingosdk.VectorWithIdVector()
        for i, v in enumerate(add_param.vectors):
            id = 0
            if add_param.ids is not None:
                id = add_param.ids[i]

            # TODO: support unit8
            tmp_vector = dingosdk.Vector(dingosdk.kFloat, len(v))
            tmp_vector.float_values = v

            vector_with_id = dingosdk.VectorWithId(id, tmp_vector)

            scarlar_data = dingosdk.ScalarDataMap()
            for key, value in add_param.datas[i].items():
                scarlar_value = dingosdk.ScalarValue()
                scarlar_value.type = sdk_types[auto_value_type(value)]

                scalar_type = scarlar_value.type
                scarlar_field = dingosdk.ScalarField()
                if scalar_type == dingosdk.kSTRING:
                    scarlar_field.string_data = value
                elif scalar_type == dingosdk.kDOUBLE:
                    scarlar_field.double_data = value
                elif scalar_type == dingosdk.kINT64:
                    scarlar_field.long_data = value
                elif scalar_type == dingosdk.kBOOL:
                    scarlar_field.bool_data = value
                else:
                    raise RuntimeError(f"not support type: {scarlar_value.type}")

                # TODO: support vector with multiple fields
                fields = dingosdk.ScalarFieldVector()
                fields.append(scarlar_field)
                scarlar_value.fields = fields

                scarlar_data[key] = scarlar_value

            vector_with_id.scalar_data = scarlar_data
            vectors.append(vector_with_id)

        s = self.vector_client.AddByIndexName(
            self.schema_id, add_param.index_name, vectors
        )

        if s.ok():
            return [sdk_vector_with_id_to_vector_with_id(v).to_dict() for v in vectors]
            # return list(map(lambda v: v.id, vectors))
        else:
            raise RuntimeError(
                f"add vector in {add_param.index_name} fail: {s.ToString()}"
            )

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
        s, count = self.vector_client.CountallByIndexName(self.schema_id, index_name)
        if s.ok():
            return count
        else:
            raise RuntimeError(f"count index {index_name} fail: {s.ToString()}")

    # TODO: unify the return
    def vector_metrics(self, index_name: str):
        """
        vector_metrics metrics in index

        Args:
            index_name (str): the name of in index

        Returns:
            str: metrics string
        """
        s, result = self.vector_client.GetIndexMetricsByIndexName(
            self.schema_id, index_name
        )
        if s.ok():
            return result.ToString()
        else:
            raise RuntimeError(f"get index {index_name} metrics fail: {s.ToString()}")

    def vector_scan(self, scan_param: VectorScanParam) -> list:
        """
        vector_scan scan with start_id

        Args:
            scan_param VectorScanParam

        Raises:
            RuntimeError: return error

        Returns:
            list:  scan info list
        """
        sdk_param = dingosdk.ScanQueryParam()
        sdk_param.vector_id_start = scan_param.start_id
        sdk_param.vector_id_end = scan_param.end_id
        sdk_param.max_scan_count = scan_param.max_count
        sdk_param.is_reverse = scan_param.is_reverse
        sdk_param.with_vector_data = scan_param.with_vector_data
        sdk_param.with_scalar_data = scan_param.with_scalar_data
        sdk_param.with_table_data = scan_param.with_table_data
        for key in scan_param.fields:
            sdk_param.selected_keys.append(key)

        if scan_param.filter_scalar:
            sdk_param.use_scalar_filter = True
            for key, value in scan_param.filter_scalar.items():
                scarlar_value = dingosdk.ScalarValue()
                scarlar_value.type = sdk_types[auto_value_type(value)]
                scalar_type = scarlar_value.type

                scarlar_field = dingosdk.ScalarField()
                if scalar_type == dingosdk.kSTRING:
                    scarlar_field.string_data = value
                elif scalar_type == dingosdk.kDOUBLE:
                    scarlar_field.double_data = value
                elif scalar_type == dingosdk.kINT64:
                    scarlar_field.long_data = value
                elif scalar_type == dingosdk.kBOOL:
                    scarlar_field.bool_data = value
                else:
                    raise RuntimeError(f"not support type: {scarlar_value.type}")

                scarlar_value.fields.append(scarlar_field)

                sdk_param.scalar_data[key] = scarlar_value

        s, result = self.vector_client.ScanQueryByIndexName(
            self.schema_id, scan_param.index_name, sdk_param
        )

        if s.ok():
            return [
                sdk_vector_with_id_to_vector_with_id(v).to_dict()
                for v in result.vectors
            ]
        else:
            raise RuntimeError(
                f"scan index {scan_param.index_name} fail: {s.ToString()}"
            )

    def vector_search(self, param: VectorSearchParam) -> list:
        """
        vector_search search vector

        Args:
            param : VectorSearchParam

        Raises:
            RuntimeError: return error

        Returns:
            List[dict]: search results
        """
        assert param.fields is not None
        assert param.search_params is not None

        sdk_param = dingosdk.SearchParam()
        sdk_param.topk = param.top_k
        sdk_param.with_vector_data = param.with_vector_data
        sdk_param.with_scalar_data = param.with_scalar_data

        for key in param.fields:
            sdk_param.selected_keys.append(key)

        # TODO: support vecotr id filter
        sdk_param.filter_source = dingosdk.kScalarFilter

        sdk_param.filter_type = dingosdk.kQueryPre
        if not param.pre_filter:
            sdk_param.filter_type = dingosdk.kQueryPost

        sdk_param.use_brute_force = param.brute

        extra_params_map = dingosdk.SearchExtraParamMap()
        extra_params_map[dingosdk.kNprobe] = param.search_params.get(
            "nprobe", constants.N_PROBES
        )
        extra_params_map[dingosdk.kRecallNum] = param.search_params.get(
            "recallNum", constants.RECALL_NUM
        )
        extra_params_map[dingosdk.kParallelOnQueries] = param.search_params.get(
            "parallelOnQueries", constants.PARALLEL_ON_QUERIES
        )
        extra_params_map[dingosdk.kEfSearch] = param.search_params.get(
            "efSearch", constants.EF_SEARCH
        )

        sdk_param.extra_params = extra_params_map

        if "meta_expr" in param.search_params.keys():
            if param.search_params["meta_expr"] is not None:
                sdk_param.langchain_expr_json = json.dumps(
                    auto_expr_type(
                        convert_dict_to_expr(param.search_params["meta_expr"])
                    ),
                    ensure_ascii=False,
                )
        elif "langchain_expr" in param.search_params.keys():
            if param.search_params["langchain_expr"] is not None:
                sdk_param.langchain_expr_json = json.dumps(
                    auto_expr_type(param.search_params["langchain_expr"]),
                    ensure_ascii=False,
                )

        target_vectors = []
        for xq in param.xq:
            # TODO: support  uint8
            tmp_vector = dingosdk.Vector(dingosdk.kFloat, len(xq))
            tmp_vector.float_values = xq

            tmp = dingosdk.VectorWithId()
            tmp.vector = tmp_vector

            target_vectors.append(tmp)

        result = dingosdk.SearchResultVector()
        s, result = self.vector_client.SearchByIndexName(
            self.schema_id, param.index_name, sdk_param, target_vectors
        )

        if s.ok():
            return [sdk_search_result_to_search_result(v).to_dict() for v in result]
        else:
            raise RuntimeError(f"search index:{param.index_name} fail: {s.ToString()}")

    def vector_get(self, param: VectorGetParam) -> list:
        """
        vector_get query vector

        Args:
            param: VectorGetParam

        Raises:
            RuntimeError: _description_

        Returns:
            list: _description_
        """
        sdk_param = dingosdk.QueryParam()
        sdk_param.vector_ids = param.ids
        sdk_param.with_vector_data = param.with_vector_data
        sdk_param.with_scalar_data = param.with_scalar_data

        result = dingosdk.QueryResult()
        s, result = self.vector_client.BatchQueryByIndexName(
            self.schema_id, param.index_name, sdk_param
        )
        if s.ok():
            return [
                sdk_vector_with_id_to_vector_with_id(v).to_dict()
                for v in result.vectors
            ]
        else:
            raise RuntimeError(
                f"vector get form index:{param.index_name} fail: {s.ToString()}"
            )

    def vector_delete(self, param: VectorDeleteParam) -> list:
        """
        vector_delete delete vector with ids

        Args:
            params: VectorDeleteParam

        Raises:
            RuntimeError: return error

        Returns:
            list : [True, False, ...]
        """
        result = dingosdk.DeleteResultVector()
        s, result = self.vector_client.DeleteByIndexName(
            self.schema_id, param.index_name, param.ids
        )

        if not s.ok():
            raise RuntimeError(
                f"vector delete form index:{param.index_name} fail: {s.ToString()}"
            )

        result_dict = {res.vector_id: res.deleted for res in result}

        delete_status = []
        for id in param.ids:
            assert id in result_dict, f"id: {id} not in result_dict"
            delete_status.append(result_dict[id])

        return delete_status
