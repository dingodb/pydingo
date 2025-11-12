#!/usr/bin/python3

import json
import dingosdk
from dingodb.sdk_client import SDKClient

from dingodb.utils.tools import auto_value_type
from dingodb.common import constants
from dingodb.common.vector_rep import (
    ScalarSchema,
    ScalarType,
    RegionState,
    RegionStatus,
)
from dingodb.utils.tools import auto_value_type, auto_expr_type, convert_dict_to_expr
from dingodb.common.document_rep import DocumentSchema ,DocumentType

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

from .sdk_vector_param_factory import SDKParamFactory
from .sdk_vector_adapter import (
    sdk_search_result_to_search_result,
    sdk_vector_with_id_to_vector_with_id,
    sdk_index_metrics_result_to_index_metric,
    sdk_err_status_result_to_err_status,
    sdk_state_result_to_state,
    type_conversion,
)

sdk_types = {
    "STRING": dingosdk.Type.kSTRING,
    "DOUBLE": dingosdk.Type.kDOUBLE,
    "INT64": dingosdk.Type.kINT64,
    "BOOL": dingosdk.Type.kBOOL,
}

scalar_type_to_document_type = {
    DocumentType.BOOL: dingosdk.Type.kBOOL,
    DocumentType.INT64: dingosdk.Type.kINT64,
    DocumentType.DOUBLE: dingosdk.Type.kDOUBLE,
    DocumentType.STRING: dingosdk.Type.kSTRING,
    DocumentType.BYTES: dingosdk.Type.kBYTES,
    DocumentType.DATETIME: dingosdk.Type.kDATETIME,
}


scalar_type_to_sdk_type = {
    ScalarType.BOOL: dingosdk.Type.kBOOL,
    ScalarType.INT64: dingosdk.Type.kINT64,
    ScalarType.DOUBLE: dingosdk.Type.kDOUBLE,
    ScalarType.STRING: dingosdk.Type.kSTRING,
}


class SDKVectorClient:
    def __init__(self, client: SDKClient):
        """
        __init__ init Client

        Args:
            client: SDKClient
        """
        self.schema_id = 2
        self.client = client.dingosdk_client

        s, self.vector_client = self.client.NewVectorClient()
        if not s.ok():
            raise RuntimeError(f"dongo vector client build fail: {s.ToString()}")

    def create_index(
        self, param: CreateIndexParam, schema: ScalarSchema = None,document_schema: DocumentSchema = None
    ) -> bool:
        """
        create_index create index

        Args:
            param (CreateIndexParam): create index param
            schema (ScalarSchema): scalar data schema

        Returns:
            bool: create index result
        """
        s, creator = self.client.NewVectorIndexCreator()
        assert s.ok(), f"dingo creator build fail: {s.ToString()}"
        creator.SetSchemaId(self.schema_id)
        creator.SetName(param.index_name)
        creator.SetReplicaNum(param.replicas)
        if param.operand is not None:
            if len(param.operand) != 0:
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
        elif index_type == "diskann":
            sdk_param = SDKParamFactory.create_diskann_param(
                index_type, param.index_config
            )
            creator.SetDiskAnnParam(sdk_param)
        elif index_type == "brute":
            sdk_param = SDKParamFactory.create_brute_param(
                index_type, param.index_config
            )
            creator.SetBruteForceParam(sdk_param)
        elif index_type == "binary_flat":
            sdk_param = SDKParamFactory.create_binary_flat_param(
                index_type, param.index_config
            )
            creator.SetBinaryFlatParam(sdk_param)
        elif index_type == "binary_ivf_flat":
            sdk_param = SDKParamFactory.create_binary_ivf_flat_param(
                index_type, param.index_config
            )
            creator.SetBinaryIvfFlatParam(sdk_param)
        else:
            raise RuntimeError(f"index_type: {index_type} not support")

        if param.auto_id:
            creator.SetAutoIncrementStart(param.start_id)

        if schema is not None and len(schema.cols) != 0:
            sdk_scalar_schem = dingosdk.VectorScalarSchema()

            for col in schema.cols:
                sdk_col = dingosdk.VectorScalarColumnSchema(
                    col.key, scalar_type_to_sdk_type[col.type], col.speed
                )

                sdk_scalar_schem.AddScalarColumn(sdk_col)

            creator.SetScalarSchema(sdk_scalar_schem)

        creator.SetEnableScalarSpeedUpWithDocument(param.enable_scalar_speed_up_with_document)
        creator.SetJsonParams(param.json_params)
            

        if document_schema is not None and len(document_schema.cols) != 0:
            document_schema_schem = dingosdk.DocumentSchema()

            for col in document_schema.cols:
                sdk_col = dingosdk.DocumentColumn(
                    col.key, scalar_type_to_document_type[col.type]
                )

                document_schema_schem.AddColumn(sdk_col)

            creator.SetDocumentSchema(document_schema_schem)
       

        # index_id = -1
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
        s = self.client.DropVectorIndexByName(self.schema_id, index_name)
        if s.ok():
            return True
        else:
            raise RuntimeError(f"delete index {index_name} fail: {s.ToString()}")

    def vectors_add_with_schema(
        self, schema_dict: dict, add_param: VectorAddParam
    ) -> list:
        vectors = []
        BITS_PER_BYTE = 8
        for i, v in enumerate(add_param.vectors):
            id = 0
            if add_param.ids is not None:
                id = add_param.ids[i]

            if add_param.value_type == "float":
                tmp_vector = dingosdk.Vector(dingosdk.ValueType.kFloat, len(v))
                tmp_vector.float_values = v
            elif add_param.value_type == "binary":
                tmp_vector = dingosdk.Vector(
                    dingosdk.ValueType.kUint8, len(v) * BITS_PER_BYTE
                )
                tmp_vector.binary_values = v

            vector_with_id = dingosdk.VectorWithId(id, tmp_vector)

            scarlar_data = {}
            for key, value in add_param.datas[i].items():

                scalar_type = sdk_types[auto_value_type(value)]

                if key in schema_dict:
                    if not type_conversion(scalar_type, schema_dict[key]):
                        raise RuntimeError(
                            f"type_conversion error {scalar_type} to {schema_dict[key]}"
                        )
                    scalar_type = schema_dict[key]

                scarlar_value = dingosdk.ScalarValue()
                scarlar_field = dingosdk.ScalarField()

                if scalar_type == dingosdk.Type.kSTRING:
                    scarlar_value.type = dingosdk.Type.kSTRING
                    scarlar_field.string_data = value
                elif scalar_type == dingosdk.Type.kDOUBLE:
                    scarlar_value.type = dingosdk.Type.kDOUBLE
                    scarlar_field.double_data = value
                elif scalar_type == dingosdk.Type.kINT64:
                    scarlar_value.type = dingosdk.Type.kINT64
                    scarlar_field.long_data = value
                elif scalar_type == dingosdk.Type.kBOOL:
                    scarlar_value.type = dingosdk.Type.kBOOL
                    scarlar_field.bool_data = value
                else:
                    raise RuntimeError(f"not support type: {scalar_type}")

                # TODO: support vector with multiple fields
                fields = []
                fields.append(scarlar_field)
                scarlar_value.fields = fields

                scarlar_data[key] = scarlar_value

            vector_with_id.scalar_data = scarlar_data
            vectors.append(vector_with_id)
        return vectors

    def vectors_add_without_schema(self, add_param: VectorAddParam) -> list:
        vectors = []
        BITS_PER_BYTE = 8
        for i, v in enumerate(add_param.vectors):
            id = 0
            if add_param.ids is not None:
                id = add_param.ids[i]

            if add_param.value_type == "float":
                tmp_vector = dingosdk.Vector(dingosdk.ValueType.kFloat, len(v))
                tmp_vector.float_values = v
            elif add_param.value_type == "binary":
                tmp_vector = dingosdk.Vector(
                    dingosdk.ValueType.kUint8, len(v) * BITS_PER_BYTE
                )
                tmp_vector.binary_values = v

            vector_with_id = dingosdk.VectorWithId(id, tmp_vector)

            scarlar_data = {}
            for key, value in add_param.datas[i].items():
                scarlar_value = dingosdk.ScalarValue()
                scarlar_value.type = sdk_types[auto_value_type(value)]

                scalar_type = scarlar_value.type
                scarlar_field = dingosdk.ScalarField()
                if scalar_type == dingosdk.Type.kSTRING:
                    scarlar_field.string_data = value
                elif scalar_type == dingosdk.Type.kDOUBLE:
                    scarlar_field.double_data = value
                elif scalar_type == dingosdk.Type.kINT64:
                    scarlar_field.long_data = value
                elif scalar_type == dingosdk.Type.kBOOL:
                    scarlar_field.bool_data = value
                else:
                    raise RuntimeError(f"not support type: {scarlar_value.type}")

                # TODO: support vector with multiple fields
                fields = []
                fields.append(scarlar_field)
                scarlar_value.fields = fields

                scarlar_data[key] = scarlar_value

            vector_with_id.scalar_data = scarlar_data
            vectors.append(vector_with_id)
        return vectors

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

        status, out_vector_index = self.client.GetVectorIndex(
            self.schema_id, add_param.index_name
        )
        if not status.ok():
            raise RuntimeError(
                f"get index {add_param.index_name} error: {status.ToString()}"
            )
        else:
            if out_vector_index.HasScalarSchema():
                schema_dict = out_vector_index.GetSchema()
                vectors = self.vectors_add_with_schema(schema_dict, add_param)
            else:
                vectors = self.vectors_add_without_schema(add_param)

        s, vectors = self.vector_client.AddByIndexName(
            self.schema_id, add_param.index_name, vectors
        )

        if s.ok():
            return [sdk_vector_with_id_to_vector_with_id(v).to_dict() for v in vectors]
        else:
            raise RuntimeError(
                f"add vector in {add_param.index_name} fail: {s.ToString()}"
            )

    def vector_upsert(self, upsert_param: VectorAddParam) -> list:
        """
        vector_upsert upsert vector

        Args:
            upsert_param: VectorAddParam

        Raises:
            RuntimeError: return error

        Returns:
            list: vector id list
        """

        status, out_vector_index = self.client.GetVectorIndex(
            self.schema_id, upsert_param.index_name
        )
        if not status.ok():
            raise RuntimeError(
                f"get index {upsert_param.index_name} error: {status.ToString()}"
            )
        else:
            if out_vector_index.HasScalarSchema():
                schema_dict = out_vector_index.GetSchema()
                vectors = self.vectors_add_with_schema(schema_dict, upsert_param)
            else:
                vectors = self.vectors_add_without_schema(upsert_param)

        s, vectors = self.vector_client.UpsertByIndexName(
            self.schema_id, upsert_param.index_name, vectors
        )

        if s.ok():
            return [sdk_vector_with_id_to_vector_with_id(v).to_dict() for v in vectors]
        else:
            raise RuntimeError(
                f"upsert vector in {upsert_param.index_name} fail: {s.ToString()}"
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
            return sdk_index_metrics_result_to_index_metric(result).to_dict()
        else:
            raise RuntimeError(f"get index {index_name} metrics fail: {s.ToString()}")

    def vectors_scan_with_schema(self, schema_dict: dict, scan_param: VectorScanParam):
        sdk_param = dingosdk.ScanQueryParam()
        sdk_param.vector_id_start = scan_param.start_id
        sdk_param.vector_id_end = scan_param.end_id
        sdk_param.max_scan_count = scan_param.max_count
        sdk_param.is_reverse = scan_param.is_reverse
        sdk_param.with_vector_data = scan_param.with_vector_data
        sdk_param.with_scalar_data = scan_param.with_scalar_data
        sdk_param.with_table_data = scan_param.with_table_data
        selected_keys = []
        for key in scan_param.fields:
            selected_keys.append(key)
        sdk_param.selected_keys = selected_keys

        if scan_param.filter_scalar:
            sdk_param.use_scalar_filter = True
            scarlar_data = {}
            for key, value in scan_param.filter_scalar.items():

                scalar_type = sdk_types[auto_value_type(value)]

                if key in schema_dict:
                    if not type_conversion(scalar_type, schema_dict[key]):
                        raise RuntimeError(
                            f"type_conversion error {scalar_type} to {schema_dict[key]}"
                        )
                    scalar_type = schema_dict[key]

                scarlar_value = dingosdk.ScalarValue()
                scarlar_field = dingosdk.ScalarField()

                if scalar_type == dingosdk.Type.kSTRING:
                    scarlar_value.type = dingosdk.Type.kSTRING
                    scarlar_field.string_data = value
                elif scalar_type == dingosdk.Type.kDOUBLE:
                    scarlar_value.type = dingosdk.Type.kDOUBLE
                    scarlar_field.double_data = value
                elif scalar_type == dingosdk.Type.kINT64:
                    scarlar_value.type = dingosdk.Type.kINT64
                    scarlar_field.long_data = value
                elif scalar_type == dingosdk.Type.kBOOL:
                    scarlar_value.type = dingosdk.Type.kBOOL
                    scarlar_field.bool_data = value
                else:
                    raise RuntimeError(f"not support type: {scalar_type}")

                # TODO: support vector with multiple fields
                fields = []
                fields.append(scarlar_field)
                scarlar_value.fields = fields

                scarlar_data[key] = scarlar_value

            sdk_param.scalar_data = scarlar_data

        return sdk_param

    def vectors_scan_without_schema(self, scan_param: VectorScanParam):
        sdk_param = dingosdk.ScanQueryParam()
        sdk_param.vector_id_start = scan_param.start_id
        sdk_param.vector_id_end = scan_param.end_id
        sdk_param.max_scan_count = scan_param.max_count
        sdk_param.is_reverse = scan_param.is_reverse
        sdk_param.with_vector_data = scan_param.with_vector_data
        sdk_param.with_scalar_data = scan_param.with_scalar_data
        sdk_param.with_table_data = scan_param.with_table_data
        selected_keys = []
        for key in scan_param.fields:
            selected_keys.append(key)
        sdk_param.selected_keys = selected_keys

        if scan_param.filter_scalar:
            sdk_param.use_scalar_filter = True
            scarlar_data = {}
            for key, value in scan_param.filter_scalar.items():
                scarlar_value = dingosdk.ScalarValue()
                scarlar_value.type = sdk_types[auto_value_type(value)]
                scalar_type = scarlar_value.type

                scarlar_field = dingosdk.ScalarField()
                if scalar_type == dingosdk.Type.kSTRING:
                    scarlar_field.string_data = value
                elif scalar_type == dingosdk.Type.kDOUBLE:
                    scarlar_field.double_data = value
                elif scalar_type == dingosdk.Type.kINT64:
                    scarlar_field.long_data = value
                elif scalar_type == dingosdk.Type.kBOOL:
                    scarlar_field.bool_data = value
                else:
                    raise RuntimeError(f"not support type: {scarlar_value.type}")

                # TODO: support vector with multiple fields
                fields = []
                fields.append(scarlar_field)
                scarlar_value.fields = fields

                scarlar_data[key] = scarlar_value

            sdk_param.scalar_data = scarlar_data

        return sdk_param

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

        status, out_vector_index = self.client.GetVectorIndex(
            self.schema_id, scan_param.index_name
        )
        if not status.ok():
            raise RuntimeError(
                f"get index {scan_param.index_name} error: {status.ToString()}"
            )
        else:
            if out_vector_index.HasScalarSchema():
                schema_dict = out_vector_index.GetSchema()
                sdk_param = self.vectors_scan_with_schema(schema_dict, scan_param)
            else:
                sdk_param = self.vectors_scan_without_schema(scan_param)

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

    def get_max_index_row(self, index_name: str) -> int:
        """
        get_max_index_row get max index row

        Args:
            index_name (str): the name of in index

        Raises:
            RuntimeError: return error

        Returns:
            int: max vector id
        """
        s, result = self.vector_client.GetIndexMetricsByIndexName(
            self.schema_id, index_name
        )
        if s.ok():
            metric = sdk_index_metrics_result_to_index_metric(result)
            return metric.max_vector_id
        else:
            raise RuntimeError(f"get index {index_name} metrics fail: {s.ToString()}")

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
        sdk_param.is_scalar_speed_up_with_document = param.is_scalar_speed_up_with_document
        sdk_param.query_string = param.query_string

        selected_keys = []
        for key in param.fields:
            selected_keys.append(key)
        sdk_param.selected_keys = selected_keys

        # TODO: support vecotr id filter
        sdk_param.filter_source = dingosdk.FilterSource.kScalarFilter

        sdk_param.filter_type = dingosdk.FilterType.kQueryPre
        if not param.pre_filter:
            sdk_param.filter_type = dingosdk.FilterType.kQueryPost

        sdk_param.use_brute_force = param.brute

        extra_params_map = {}
        extra_params_map[dingosdk.SearchExtraParamType.kNprobe] = (
            param.search_params.get("nprobe", constants.N_PROBES)
        )
        extra_params_map[dingosdk.SearchExtraParamType.kRecallNum] = (
            param.search_params.get("recallNum", constants.RECALL_NUM)
        )
        extra_params_map[dingosdk.SearchExtraParamType.kParallelOnQueries] = (
            param.search_params.get("parallelOnQueries", constants.PARALLEL_ON_QUERIES)
        )
        extra_params_map[dingosdk.SearchExtraParamType.kEfSearch] = (
            param.search_params.get("efSearch", constants.EF_SEARCH)
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
        BITS_PER_BYTE = 8
        for xq in param.xq:

            if param.value_type == "float":
                tmp_vector = dingosdk.Vector(dingosdk.ValueType.kFloat, len(xq))
                tmp_vector.float_values = xq
            elif param.value_type == "binary":
                tmp_vector = dingosdk.Vector(
                    dingosdk.ValueType.kUint8, len(xq) * BITS_PER_BYTE
                )
                tmp_vector.binary_values = xq

            tmp = dingosdk.VectorWithId()
            tmp.vector = tmp_vector

            target_vectors.append(tmp)

        s, result = self.vector_client.SearchByIndexName(
            self.schema_id, param.index_name, sdk_param, target_vectors
        )

        if s.ok():
            search_result = [sdk_search_result_to_search_result(v) for v in result]

            empty = True
            for s in search_result:
                if not s.is_empty():
                    empty = False
                    break

            if empty:
                return []
            else:
                return [s.to_dict() for s in search_result]

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
        sdk_param.vector_ids = list(set(param.ids))
        sdk_param.with_vector_data = param.with_vector_data
        sdk_param.with_scalar_data = param.with_scalar_data

        # result = dingosdk.QueryResult()
        s, result = self.vector_client.BatchQueryByIndexName(
            self.schema_id, param.index_name, sdk_param
        )
        if s.ok():
            get_results = {
                v.id: sdk_vector_with_id_to_vector_with_id(v) for v in result.vectors
            }

            return_result = []
            for id in param.ids:
                if id in get_results:
                    return_result.append(get_results[id].to_dict())
                else:
                    return_result.append(None)
            return return_result
        else:
            raise RuntimeError(
                f"vector get form index:{param.index_name} fail: {s.ToString()}"
            )

    def vector_delete(self, param: VectorDeleteParam) -> list:
        """
        vector_delete delete vector with ids

        Args:
            param: VectorDeleteParam

        Raises:
            RuntimeError: return error

        Returns:
            list : [True, False, ...]
        """
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
        s, result = self.vector_client.StatusByIndexName(self.schema_id, index_name)
        if not s.ok():
            raise RuntimeError(
                f"vector status by index form index:{index_name} fail: {s.ToString()}"
            )
        status_state = sdk_state_result_to_state(result)
        return status_state

        # return [s.to_dict() for s in status_state]

    def vector_status_by_region(
        self, param: VectorStatusByRegionIdParam
    ) -> list[RegionState]:
        """
        vector_status_by_region

        Args:
             param: VectorStatusByRegionIdParam

        Raises:
            RuntimeError: return error

        Returns:
            list: state list
        """

        s, result = self.vector_client.StatusByRegionIdIndexName(
            self.schema_id, param.index_name, param.ids
        )

        if not s.ok():
            raise RuntimeError(
                f"vector status by region  form index:{param.index_name} fail: {s.ToString()}"
            )
        status_state = sdk_state_result_to_state(result)
        return status_state

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
        s, result = self.vector_client.BuildByIndexName(self.schema_id, index_name)
        if not s.ok() and not s.IsBuildFailed():
            raise RuntimeError(
                f"vector build by index form index:{index_name} fail: {s.ToString()}"
            )
        build_status = sdk_err_status_result_to_err_status(result)
        return build_status

    def vector_build_by_region(
        self, param: VectorBuildByRegionIdParam
    ) -> list[RegionStatus]:
        """
        vector_build_by_index

        Args:
            param: VectorBuildByRegionIdParam

        Raises:
            RuntimeError: return error

        Returns:
            list: err_status list
        """

        s, result = self.vector_client.BuildByRegionIdIndexName(
            self.schema_id, param.index_name, param.ids
        )

        if not s.ok() and not s.IsBuildFailed():
            raise RuntimeError(
                f"vector build by region  form index:{param.index_name} fail: {s.ToString()}"
            )
        build_status = sdk_err_status_result_to_err_status(result)
        return build_status

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
        s, result = self.vector_client.LoadByIndexName(self.schema_id, index_name)
        if not s.ok() and not s.IsLoadFailed():
            raise RuntimeError(
                f"vector load by index form index:{index_name} fail: {s.ToString()}"
            )
        load_status = sdk_err_status_result_to_err_status(result)
        return load_status

    def vector_load_by_region(
        self, param: VectorLoadByRegionIdParam
    ) -> list[RegionStatus]:
        """
        vector_load_by_region

        Args:
            param: VectorLoadByRegionIdParam

        Raises:
            RuntimeError: return error

        Returns:
            list: err_status list
        """

        s, result = self.vector_client.LoadByRegionIdIndexName(
            self.schema_id, param.index_name, param.ids
        )

        if not s.ok() and not s.IsLoadFailed():
            raise RuntimeError(
                f"vector load by region  form index:{param.index_name} fail: {s.ToString()}"
            )
        load_status = sdk_err_status_result_to_err_status(result)
        return load_status

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
        s, result = self.vector_client.ResetByIndexName(self.schema_id, index_name)
        if not s.ok() and not s.IsResetFailed():
            raise RuntimeError(
                f"vector reset by index form index:{index_name} fail: {s.ToString()}"
            )
        reset_status = sdk_err_status_result_to_err_status(result)
        return reset_status

    def vector_reset_by_region(
        self, param: VectorResetByRegionIdParam
    ) -> list[RegionStatus]:
        """
        vector_reset_by_region

        Args:
            param: VectorResetByRegionIdParam

        Raises:
            RuntimeError: return error

        Returns:
            list: err_status list
        """

        s, result = self.vector_client.ResetByRegionIdIndexName(
            self.schema_id, param.index_name, param.ids
        )

        if not s.ok() and not s.IsResetFailed():
            raise RuntimeError(
                f"vector reset by region  form index:{param.index_name} fail: {s.ToString()}"
            )
        reset_status = sdk_err_status_result_to_err_status(result)
        return reset_status

    def vector_import_add(self, add_param: VectorAddParam) -> list:
        """
        vector_import_add add vector

        Args:
            add_param: VectorAddParam

        Raises:
            RuntimeError: return error

        Returns:
            list: vector id list
        """
        status, out_vector_index = self.client.GetVectorIndex(
            self.schema_id, add_param.index_name
        )
        if not status.ok():
            raise RuntimeError(
                f"get index {add_param.index_name} error: {status.ToString()}"
            )
        else:
            if out_vector_index.HasScalarSchema():
                schema_dict = out_vector_index.GetSchema()
                vectors = self.vectors_add_with_schema(schema_dict, add_param)
            else:
                vectors = self.vectors_add_without_schema(add_param)

        s, vectors = self.vector_client.ImportAddByIndexName(
            self.schema_id, add_param.index_name, vectors
        )

        if s.ok():
            return [sdk_vector_with_id_to_vector_with_id(v).to_dict() for v in vectors]
        else:
            raise RuntimeError(
                f"add vector in {add_param.index_name} fail: {s.ToString()}"
            )

    def vector_import_delete(self, param: VectorDeleteParam):
        """
        vector_import_delete delete vector with ids

        Args:
            param: VectorDeleteParam

        Raises:
            RuntimeError: return error

        Returns:

        """
        s = self.vector_client.ImportDeleteByIndexName(
            self.schema_id, param.index_name, param.ids
        )

        if not s.ok():
            raise RuntimeError(
                f"vector delete form index:{param.index_name} fail: {s.ToString()}"
            )

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
        s, result = self.vector_client.CountMemoryByIndexName(
            self.schema_id, index_name
        )
        if s.ok():
            return result
        else:
            raise RuntimeError(
                f"vector count memory form index:{index_name} fail: {s.ToString()}"
            )

    def vector_get_auto_increment_memory(self, index_name: str) -> int:
        """
        vector_get_auto_increment_id get_auto_increment_id

        Args:
           index_name: str

        Raises:
            RuntimeError: return error

        Returns:
            auto_increment_id
        """
        s, result = self.vector_client.GetAutoIncrementIdByIndexName(
            self.schema_id, index_name
        )
        if s.ok():
            return result
        else:
            raise RuntimeError(
                f"vector count memory form index:{index_name} fail: {s.ToString()}"
            )

    def vector_update_auto_increment_id(self, index_name: str, start_id: int):
        """
        vector_update_auto_increment_id update AutoIncrementId

        Args:
           index_name: str

        Raises:
            RuntimeError: return error

        Returns:

        """
        s = self.vector_client.UpdateAutoIncrementIdByIndexName(
            self.schema_id, index_name, start_id
        )
        if not s.ok():
            raise RuntimeError(
                f"vector count memory form index:{index_name} fail: {s.ToString()}"
            )

    def vector_dump(self, index_name: str) -> list[str]:
        s, result = self.vector_client.DumpByIndexName(self.schema_id, index_name)

        if not s.ok():
            raise RuntimeError(
                f"vector dump form index:{index_name} fail: {s.ToString()}"
            )

        return result
