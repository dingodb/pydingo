import dingosdk

from dingodb.common.document_rep import (
    DocumentType,
    DocValue,
    Document,
    DocWithId,
    DocWithScore,
    AddResult,
    DocSearchResult,
    DocQueryResult,
    DocScanQueryResult,
    DocIndexMetricsResult,
    DocDeleteResult
)

from typing import List, Dict

document_type_to_scalar_type = {
    dingosdk.Type.kBOOL: DocumentType.BOOL,
    dingosdk.Type.kINT64: DocumentType.INT64,
    dingosdk.Type.kDOUBLE: DocumentType.DOUBLE,
    dingosdk.Type.kSTRING: DocumentType.STRING,
    dingosdk.Type.kBYTES: DocumentType.BYTES,
    dingosdk.Type.kDATETIME: DocumentType.DATETIME,
}


def document_doc_value_to_doc_value(
        document_doc_value: dingosdk.DocValue
):
    if document_doc_value.GetType() == dingosdk.Type.kINT64:
        return DocValue(DocumentType.INT64, document_doc_value.IntValue())
    elif document_doc_value.GetType() == dingosdk.Type.kDOUBLE:
        return DocValue(DocumentType.DOUBLE, document_doc_value.DoubleValue())
    elif document_doc_value.GetType() == dingosdk.Type.kSTRING:
        return DocValue(DocumentType.STRING, document_doc_value.StringValue())
    elif document_doc_value.GetType() == dingosdk.Type.kBYTES:
        return DocValue(DocumentType.BYTES, document_doc_value.BytesValue())
    elif document_doc_value.GetType() == dingosdk.Type.kBOOL:
        return DocValue(DocumentType.BOOL, document_doc_value.BoolValue())
    elif document_doc_value.GetType() == dingosdk.Type.kDATETIME:
        return DocValue(DocumentType.DATETIME, document_doc_value.DatetimeValue())
    else:
        raise RuntimeError(f"not support type: {document_doc_value.GetType()}")


def document_document_to_document(
        document_document: dingosdk.Document
):
    fields_result = {}
    fields = document_document.GetFields()
    for key, value in fields.items():
        fields_result[key] = document_doc_value_to_doc_value(value)

    return Document(fields_result)


def document_doc_with_id_to_doc_with_id(
        document_doc_with_id: dingosdk.DocWithId
):
    return DocWithId(
        id=document_doc_with_id.id,
        doc=document_document_to_document(document_doc_with_id.doc)
    )


def document_doc_with_score_to_doc_with_score(
        document_doc_with_score: dingosdk.DocWithStore
):
    return DocWithScore(
        id=document_doc_with_score.doc_with_id.id,
        doc=document_document_to_document(document_doc_with_score.doc_with_id.doc),
        score=document_doc_with_score.score
    )


def document_add_result_to_add_result(
        document_add_result: List[dingosdk.DocWithId]
):
    return AddResult(
        docs=[
            document_doc_with_id_to_doc_with_id(x) for x in document_add_result
        ]
    )


def document_search_result_to_search_result(
        document_query_result: dingosdk.DocSearchResult
):
    return DocSearchResult(
        docs=[
            document_doc_with_score_to_doc_with_score(x)
            for x in document_query_result.doc_sores
        ]
    )




def document_scan_query_result_to_scan_query_result(
        document_scan_query_result: dingosdk.DocScanQueryResult
):
    return DocScanQueryResult(
        docs=[
            document_doc_with_id_to_doc_with_id(x)
            for x in document_scan_query_result.docs
        ]
    )


def document_get_index_metrics_to_get_index_metrics(
        document_get_index_metrics: dingosdk.DocIndexMetricsResult,
) -> DocIndexMetricsResult:
    return DocIndexMetricsResult(
        total_num_docs=document_get_index_metrics.total_num_docs,
        total_num_tokens=document_get_index_metrics.total_num_tokens,
        max_doc_id=document_get_index_metrics.max_doc_id,
        min_doc_id=document_get_index_metrics.min_doc_id,
        meta_json=document_get_index_metrics.meta_json,
        json_parameter=document_get_index_metrics.json_parameter
    )


def document_delete_result_to_delete_result(
        document_delete_result: dingosdk.DocDeleteResult,
) -> DocDeleteResult:
    return DocDeleteResult(
        doc_id=document_delete_result.doc_id,
        deleted=document_delete_result.deleted
    )
