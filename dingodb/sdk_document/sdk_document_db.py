from typing import List, Dict, Union

from dingodb.sdk_client import SDKClient
from dingodb.sdk_document.sdk_document_client import SDKDocumentClient

from dingodb.common.document_rep import (
    DocumentSchema,
    AddResult,
    DocSearchResult,
    DocQueryResult,
    DocScanQueryResult,
    DocIndexMetricsResult,
    DocDeleteResult,
)

from .sdk_document_param import (
    CreateIndexParam,
    DocumentDeleteParam,
    DocumentAddParam,
    DocumentSearchParam,
    DocumentQueryParam,
    DocumentGetBorderParam,
    DocumentScanQueryParam,
    DocumentCountParam,
)


class SDKDocumentDingoDB:
    def __init__(self, client: SDKClient):
        """
        __init__ init DingoSDK

        Args:
            client: SDKClient
        """
        self.client = SDKDocumentClient(client)

    def create_index(
        self,
        index_name: str,
        schema: DocumentSchema,
        replicas: int = 3,
        operand: List[int] = None,
        start_id: int = 0,
        json_params: str = "",
    ) -> bool:
        """
        create_index create index

        Args:
            index_name (str): the name of index
            schema (DocumentSchema): the schema of index
            replicas (int, optional): dingoDB store replicas. Defaults to 3.
            operand (list, optional): operand. Defaults to None.
            start_id (int, optional): autoIncrement start id. Defaults to 0.
            json_params (str, optional): the json params of index. Defaults to "".

        Raises:
            RuntimeError: return error

        Returns:
            bool: create table status
        """
        params = CreateIndexParam(
            index_name=index_name,
            replicas=replicas,
            operand=operand,
            start_id=start_id,
            json_params=json_params,
        )

        return self.client.create_index(params, schema=schema)

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

    def get_schema(self, index_name: str) -> DocumentSchema:
        """
        get_schema get dschema

        Args:
            index_name (str): the name of index

        Raises:
            RuntimeError: return error

        Returns:
            DocumentSchema: dingodb.common.document_rep.DocumentSchema
        """

        return self.client.get_schema(index_name)

    def document_add(
        self, index_name: str, documents: List, ids: List[int] = None
    ) -> AddResult:
        """
        document_add add document

        Args:
            index_name (str): the name of index
            documents (list): documents list
            ids (list): id list

        Raises:
            RuntimeError: return error

        Returns:
            AddResult: dingodb.common.document_rep.AddResult
        """
        params = DocumentAddParam(index_name=index_name, documents=documents, ids=ids)

        return self.client.document_add(params)

    def document_search(
        self,
        index_name: str,
        query_string: str,
        top_n: int,
        doc_ids: List = None,
        with_scalar_data: bool = False,
        column_names: List[str] = None,
        selected_keys: List[str] = None,
    ) -> DocSearchResult:
        """
        document_search search document

        Args:
            index_name (str): the name of the index
            query_string (str): the query string
            top_n (int, optional): top n search. Defaults to 0.
            doc_ids (list, optional): document ids. Defaults to None.
            with_scalar_data (bool, optional): whether to include scalar data. Defaults to True.
            column_names (list, optional): column names. Defaults to None.
            selected_keys (list, optional): selected keys. Defaults to None.

        Raises:
            RuntimeError: return error

        Returns:
            DocSearchResult: dingodb.common.document_rep.DocSearchResult
        """

        params = DocumentSearchParam(
            index_name=index_name,
            query_string=query_string,
            top_n=top_n,
            doc_ids=doc_ids,
            with_scalar_data=with_scalar_data,
            column_names=column_names,
            selected_keys=selected_keys,
        )

        return self.client.document_search(params)

    def document_search_all(
        self,
        index_name: str,
        query_string: str,
        top_n: int = 1,
        doc_ids: List = None,
        with_scalar_data: bool = False,
        column_names: List[str] = None,
        selected_keys: List[str] = None,
        query_limit: int = 40960,
    ) -> DocSearchResult:
        """
        document_search_all search document

        Args:
            index_name (str): the name of the index
            query_string (str): the query string
            top_n (int, optional): top n search. Defaults to 1 , is useless.
            doc_ids (list, optional): document ids. Defaults to None.
            with_scalar_data (bool, optional): whether to include scalar data. Defaults to True.
            column_names (list, optional): column names. Defaults to None.
            selected_keys (list, optional): selected keys. Defaults to None.
            query_limit (int, optional): query limit. Defaults to 40960.

        Raises:
            RuntimeError: return error

        Returns:
            DocSearchResult: dingodb.common.document_rep.DocSearchResult
        """

        params = DocumentSearchParam(
            index_name=index_name,
            query_string=query_string,
            top_n=top_n,
            doc_ids=doc_ids,
            with_scalar_data=with_scalar_data,
            column_names=column_names,
            selected_keys=selected_keys,
            query_limit=query_limit,
        )

        return self.client.document_search_all(params)

    def document_query(
        self,
        index_name: str,
        doc_ids: List,
        with_scalar_data: bool = False,
        selected_keys: List = None,
    ) -> DocQueryResult:
        """
        document_query query document

        Args:
            index_name (str): the name of the index
            doc_ids (list): document ids.
            with_scalar_data (bool, optional): whether to include scalar data. Defaults to False. if true, response with scalar data
            selected_keys (list, optional): selected keys. Defaults to None.
                If with_scalar_data is true, selected_keys is used to select scalar data, and if this parameter is null, all scalar data will be returned.

        Raises:
            RuntimeError: return error

        Returns:
            DocQueryResult: dingodb.common.document_rep.DocQueryResult
        """

        params = DocumentQueryParam(
            index_name=index_name,
            doc_ids=doc_ids,
            with_scalar_data=with_scalar_data,
            selected_keys=selected_keys,
        )

        return self.client.document_query(params)

    def document_get_border(
        self,
        index_name: str,
        is_max: bool = True,
    ) -> int:
        """
        document_get_border get_border document

        Args:
            index_name (str): the name of the index
            is_max (bool, optional): whether to return max. Defaults to True.

        Raises:
            RuntimeError: return error

        Returns:
            int: get_border results
        """

        params = DocumentGetBorderParam(index_name=index_name, is_max=is_max)

        return self.client.document_get_border(params)

    def document_scan_query(
        self,
        index_name: str,
        doc_id_start: int,
        doc_id_end: int = 0,
        is_reverse: bool = False,
        max_scan_count: int = 1000,
        with_scalar_data: bool = True,
        selected_keys: List[str] = None,
    ) -> DocScanQueryResult:
        """
        document_scan_query scan_query document

        Args:
            index_name (str): the name of the index
            doc_id_start (int): start document id
            doc_id_end (int): end document id, the end id of scan
                if is_reverse is true, doc_id_end must be less than doc_id_start
                if is_reverse is false, doc_id_end must be greater than doc_id_start
                the real range is [start, end], include start and end
                if doc_id_end == 0, scan to the end of the region
            is_reverse is true, doc_id_end must be greater than doc_id_start
            max_scan_count (int, optional): maximum number of scans. Defaults to 1000.
            with_scalar_data (bool, optional): whether to include scalar data. Defaults to False.
            selected_keys (list, optional): selected keys. Defaults to None.
                If with_scalar_data is true, selected_keys is used to select scalar data, and if this parameter is null, all scalar data will be returned.

        Raises:
            RuntimeError: return error

        Returns:
            DocScanQueryResult: dingodb.common.document_rep.DocScanQueryResult
        """

        params = DocumentScanQueryParam(
            index_name=index_name,
            doc_id_start=doc_id_start,
            doc_id_end=doc_id_end,
            is_reverse=is_reverse,
            max_scan_count=max_scan_count,
            with_scalar_data=with_scalar_data,
            selected_keys=selected_keys,
        )

        return self.client.document_scan_query(params)

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
        return self.client.document_index_metrics(index_name)

    def document_count(
        self,
        index_name: str,
        doc_id_start: int,
        doc_id_end: int,
    ) -> int:
        """
        document_count count in index

        Args:
            index_name (str): the name of in index
            doc_id_start (int): start document id
            doc_id_end (int): end document id, the end id of scan

        Raises:
            RuntimeError: return error

        Returns:
            int: count int
        """

        params = DocumentCountParam(
            index_name=index_name, doc_id_start=doc_id_start, doc_id_end=doc_id_end
        )

        return self.client.document_count(params)

    def document_delete(self, index_name: str, ids: List) -> List[bool]:
        """
        document_delete delete document with ids

        Args:
            index_name (str): the name of the index
            ids (list): id list

        Raises:
            RuntimeError: return error

        Returns:
            List[bool]: [True, False, ...]
        """
        params = DocumentDeleteParam(index_name=index_name, ids=ids)
        document_del_map = {
            d.doc_id: d.deleted for d in self.client.document_delete(params)
        }

        return [document_del_map.get(i) for i in params.ids]

    def document_get_auto_increment_id(self, index_name: str) -> int:
        """
        document_get_auto_increment_id get_auto_increment_id

        Args:
           index_name: str

        Raises:
            RuntimeError: return error

        Returns:
            auto_increment_id
        """
        return self.client.document_get_auto_increment_memory(index_name=index_name)

    def document_update_auto_increment_id(self, index_name: str, start_id: int):
        """
        document_update_auto_increment_id update AutoIncrementId

        Args:
           index_name: str

        Raises:
            RuntimeError: return error

        Returns:

        """
        return self.client.document_update_auto_increment_id(
            index_name=index_name, start_id=start_id
        )
