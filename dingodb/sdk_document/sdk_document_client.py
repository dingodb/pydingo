import dingosdk

from dingodb.sdk_client import SDKClient
from dingodb.common.document_rep import (
    DocumentType,
    DocumentSchema,
    AddResult,
    DocSearchResult,
    DocQueryResult,
    DocScanQueryResult,
    DocIndexMetricsResult,
    DocDeleteResult
)

from .sdk_document_param import (
    CreateIndexParam,
    DocumentDeleteParam,
    DocumentAddParam,
    DocumentSearchParam,
    DocumentQueryParam,
    DocumentGetBorderParam,
    DocumentScanQueryParam,
    DocumentCountParam
)

from .sdk_document_adapter import (
    document_add_result_to_add_result,
    document_search_result_to_search_result,
    document_query_result_to_query_result,
    document_scan_query_result_to_scan_query_result,
    document_get_index_metrics_to_get_index_metrics,
    document_delete_result_to_delete_result
)

from typing import List, Dict

scalar_type_to_document_type = {
    DocumentType.BOOL: dingosdk.Type.kBOOL,
    DocumentType.INT64: dingosdk.Type.kINT64,
    DocumentType.DOUBLE: dingosdk.Type.kDOUBLE,
    DocumentType.STRING: dingosdk.Type.kSTRING,
    DocumentType.BYTES: dingosdk.Type.kBYTES,
}


class SDKDocumentClient:
    def __init__(self, client: SDKClient):
        """
        __init__ init Client

        Args:
            client: SDKClient
        """
        self.schema_id = 2
        self.client = client.dingosdk_client

        s, self.document_client = self.client.NewDocumentClient()
        if not s.ok():
            raise RuntimeError(f"dongo document client build fail: {s.ToString()}")

    def create_index(
            self, param: CreateIndexParam, schema: DocumentSchema = None
    ) -> bool:
        """
        create_index create index

        Args:
            param (CreateIndexParam): create index param
            schema (DocumentSchema): scalar data schema

        Returns:
            bool: create index result
        """
        s, creator = self.client.NewDocumentIndexCreator()
        assert s.ok(), f"dingo creator build fail: {s.ToString()}"
        creator.SetSchemaId(self.schema_id)
        creator.SetName(param.index_name)
        creator.SetReplicaNum(param.replicas)
        if param.operand is not None:
            if len(param.operand) != 0:
                creator.SetRangePartitions(param.operand)

        if param.json_params != "":
            creator.SetJsonParams(param.json_params)

        if param.start_id:
            creator.SetAutoIncrementStart(param.start_id)

        if schema is not None and len(schema.cols) != 0:
            sdk_scalar_schem = dingosdk.DocumentSchema()

            for col in schema.cols:
                sdk_col = dingosdk.DocumentColumn(
                    col.key, scalar_type_to_document_type[col.type]
                )

                sdk_scalar_schem.AddColumn(sdk_col)

            creator.SetSchema(sdk_scalar_schem)

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
        s = self.client.DropDocumentIndexByName(self.schema_id, index_name)
        if s.ok():
            return True
        else:
            raise RuntimeError(f"delete index {index_name} fail: {s.ToString()}")

    def document_add(self, add_param: DocumentAddParam) -> AddResult:
        """
        document_add add document

        Args:
            add_param: DocumentAddParam

        Raises:
            RuntimeError: return error

        Returns:
            AddResult: dingodb.common.document_rep.AddResult
        """
        documents = []
        schema_dict = self.client.GetDocumentIndex(self.schema_id, add_param.index_name)[1].GetSchema()
        for i, v in enumerate(add_param.documents):
            id = 0
            if add_param.ids is not None:
                id = add_param.ids[i]

            tmp_document = dingosdk.Document()
            for key, value in add_param.documents[i].items():
                if schema_dict[key] == dingosdk.Type.kINT64:
                    tmp_document.AddField(key, dingosdk.DocValue.FromInt(value))
                elif schema_dict[key] == dingosdk.Type.kDOUBLE:
                    tmp_document.AddField(key, dingosdk.DocValue.FromDouble(value))
                elif schema_dict[key] == dingosdk.Type.kSTRING:
                    tmp_document.AddField(key, dingosdk.DocValue.FromString(value))
                elif schema_dict[key] == dingosdk.Type.kBYTES:
                    tmp_document.AddField(key, dingosdk.DocValue.FromBytes(value))
                else:
                    raise RuntimeError(f"not support type: {schema_dict[key]}")

            document_with_id = dingosdk.DocWithId(id, tmp_document)
            documents.append(document_with_id)

        s, documents = self.document_client.AddByIndexName(
            self.schema_id, add_param.index_name, documents
        )

        if s.ok():
            return document_add_result_to_add_result(documents)

        else:
            raise RuntimeError(
                f"add document in {add_param.index_name} fail: {s.ToString()}"
            )

    def document_search(self, param: DocumentSearchParam) -> DocSearchResult:
        """
        document_search search document

        Args:
            param : DocumentSearchParam

        Raises:
            RuntimeError: return error

        Returns:
            DocSearchResult: dingodb.common.document_rep.DocSearchResult
        """

        document_param = dingosdk.DocSearchParam()
        document_param.query_string = param.query_string
        document_param.top_n = param.top_n

        document_param.use_id_filter = param.use_id_filter
        if param.use_id_filter:
            document_param.doc_ids = param.doc_ids

        document_param.with_scalar_data = param.with_scalar_data

        if param.column_names:
            document_param.column_names = param.column_names
        if param.selected_keys:
            document_param.selected_keys = param.selected_keys

        s, result = self.document_client.SearchByIndexName(
            self.schema_id, param.index_name, document_param
        )

        if s.ok():
            # print(result.ToString())
            return document_search_result_to_search_result(result)
        else:
            raise RuntimeError(f"search index:{param.index_name} fail: {s.ToString()}")

    def document_query(self, param: DocumentQueryParam) -> DocQueryResult:
        """
        document_query query document

        Args:
            param : DocumentQueryParam

        Raises:
            RuntimeError: return error

        Returns:
            DocQueryResult: dingodb.common.document_rep.DocQueryResult
        """
        document_param = dingosdk.DocQueryParam()
        document_param.doc_ids = param.doc_ids
        document_param.with_scalar_data = param.with_scalar_data
        if param.selected_keys:
            document_param.selected_keys = param.selected_keys

        s, result = self.document_client.BatchQueryByIndexName(
            self.schema_id, param.index_name, document_param
        )

        if s.ok():
            # print(result.ToString())
            return document_query_result_to_query_result(result)
        else:
            raise RuntimeError(f"query index:{param.index_name} fail: {s.ToString()}")

    def document_get_border(self, param: DocumentGetBorderParam) -> int:
        """
        document_get_border get_border document

        Args:
            param : DocumentGetBorderParam

        Raises:
            RuntimeError: return error

        Returns:
            List[dict]: get_border results
        """
        s, result = self.document_client.GetBorderByIndexName(
            self.schema_id, param.index_name, param.is_max
        )

        if s.ok():
            return result
        else:
            raise RuntimeError(f"get_border index:{param.index_name} fail: {s.ToString()}")

    def document_scan_query(self, param: DocumentScanQueryParam) -> DocScanQueryResult:
        """
        document_scan_query scan_query document

        Args:
            param : DocumentScanQueryParam

        Raises:
            RuntimeError: return error

        Returns:
            DocScanQueryResult: dingodb.common.document_rep.DocScanQueryResult
        """
        document_param = dingosdk.DocScanQueryParam()
        document_param.doc_id_start = param.doc_id_start
        document_param.doc_id_end = param.doc_id_end
        document_param.is_reverse = param.is_reverse
        document_param.max_scan_count = param.max_scan_count

        document_param.with_scalar_data = param.with_scalar_data
        if param.selected_keys:
            document_param.selected_keys = param.selected_keys

        s, result = self.document_client.ScanQueryByIndexName(
            self.schema_id, param.index_name, document_param
        )

        if s.ok():
            # print(result.ToString())
            return document_scan_query_result_to_scan_query_result(result)
        else:
            raise RuntimeError(f"scan_query index:{param.index_name} fail: {s.ToString()}")

    def document_index_metrics(self, index_name: str) -> DocIndexMetricsResult:
        """
        document_index_metrics index_metrics in index

        Args:
            index_name (str): the name of in index

        Raises:
            RuntimeError: return error

        Returns:
            DocIndexMetricsResult: dingodb.common.document_rep.DocIndexMetricsResult
        """
        s, result = self.document_client.GetIndexMetricsByIndexName(
            self.schema_id, index_name
        )
        if s.ok():
            # print(result.ToString())
            return document_get_index_metrics_to_get_index_metrics(result)
        else:
            raise RuntimeError(f"get index {index_name} metrics fail: {s.ToString()}")

    def document_count(self, param: DocumentCountParam) -> int:
        """
        document_count count document

        Args:
            param : DocumentCountParam

        Raises:
            RuntimeError: return error

        Returns:
            int: count int
        """
        s, result = self.document_client.CountByIndexName(
            self.schema_id, param.index_name, param.doc_id_start, param.doc_id_end
        )

        if s.ok():
            return result
        else:
            raise RuntimeError(f"count index:{param.index_name} fail: {s.ToString()}")

    def document_delete(self, param: DocumentDeleteParam) -> List[DocDeleteResult]:
        """
        document_delete delete document with ids

        Args:
            params: DocumentDeleteParam

        Raises:
            RuntimeError: return error

        Returns:
            List[DocDeleteResult] : dingodb.common.document_rep.DocDeleteResult
        """
        s, result = self.document_client.DeleteByIndexName(
            self.schema_id, param.index_name, param.ids
        )

        if s.ok():
            # print([res.ToString() for res in result])
            return [document_delete_result_to_delete_result(res) for res in result]
        else:
            raise RuntimeError(
                f"document delete form index:{param.index_name} fail: {s.ToString()}"
            )
