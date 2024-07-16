from enum import Enum

from typing import List, Dict, Union


class DocumentType(Enum):
    BOOL = "BOOL"
    INT64 = "INT64"
    DOUBLE = "DOUBLE"
    STRING = "STRING"
    BYTES = "BYTES"


class DocumentColumn:
    def __init__(self, key: str, type: DocumentType) -> None:
        self.key = key
        self.type = type


class DocumentSchema:
    def __init__(self):
        self.cols = []

    def add_document_column(self, col: DocumentColumn):
        self.cols.append(col)


class DocValue:
    def __init__(
            self,
            type: DocumentType,
            value: Union[int, float, str]
    ):
        self.type = type
        self.value = value

    def to_dict(self):
        return {"type": self.type.value, "value": self.value}


class Document:
    def __init__(
            self,
            fields: Dict[str, DocValue]
    ):
        self.fields = fields

    def to_dict(self):
        return {key: value.to_dict() for key, value in self.fields.items()}


class DocWithId:
    def __init__(
            self,
            id: int,
            doc: Document
    ):
        self.id = id
        self.doc = doc

    def to_dict(self):
        return {
            "id": self.id,
            "doc": self.doc.to_dict()
        }


class DocWithScore:
    def __init__(
            self,
            id: int,
            doc: Document,
            score: float
    ):
        self.id = id
        self.doc = doc
        self.score = score

    def to_dict(self):
        return {
            "id": self.id,
            "doc": self.doc.to_dict(),
            "score": self.score
        }


class AddResult:
    def __init__(
            self,
            docs: List[DocWithId]
    ):
        self.docs = docs

    def to_dict(self):
        return [doc.to_dict() for doc in self.docs]


class DocSearchResult:
    def __init__(
            self,
            docs: List[DocWithScore]
    ):
        self.docs = docs

    def to_dict(self):
        return [doc.to_dict() for doc in self.docs]


class DocQueryResult:
    def __init__(
            self,
            docs: List[DocWithId]
    ):
        self.docs = docs

    def to_dict(self):
        return [doc.to_dict() for doc in self.docs]


class DocScanQueryResult:
    def __init__(
            self,
            docs: List[DocWithId]
    ):
        self.docs = docs

    def to_dict(self):
        return [doc.to_dict() for doc in self.docs]


class DocIndexMetricsResult:
    def __init__(
            self,
            total_num_docs: int,
            total_num_tokens: int,
            max_doc_id: int,
            min_doc_id: int,
            meta_json: int,
            json_parameter: bool
    ):
        self.total_num_docs = total_num_docs
        self.total_num_tokens = total_num_tokens
        self.max_doc_id = max_doc_id
        self.min_doc_id = min_doc_id
        self.meta_json = meta_json
        self.json_parameter = json_parameter

    def to_dict(self):
        return {
            "total_num_docs": self.total_num_docs,
            "total_num_tokens": self.total_num_tokens,
            "max_doc_id": self.max_doc_id,
            "min_doc_id": self.min_doc_id,
            "meta_json": self.meta_json,
            "json_parameter": self.json_parameter
        }


class DocDeleteResult:
    def __init__(
            self,
            doc_id: int,
            deleted: bool
    ):
        self.doc_id = doc_id
        self.deleted = deleted

    def to_dict(self):
        return {
            "doc_id": self.doc_id,
            "deleted": self.deleted
        }
