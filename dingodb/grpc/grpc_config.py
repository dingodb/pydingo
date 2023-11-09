from dingodb.protos.proxy_common_pb2 import *
from google.protobuf.json_format import MessageToDict

metric_type = {
    "euclidean": METRIC_TYPE_L2,
    "dotproduct": METRIC_TYPE_INNER_PRODUCT,
    "cosine": METRIC_TYPE_COSINE,
}

# proto
index_config = {
    "flat": MessageToDict(
        VectorIndexParameter(
            flat_parameter=CreateFlatParam(dimension=None, metric_type=None),
            vector_index_type=VECTOR_INDEX_TYPE_FLAT,
        ),
        including_default_value_fields=True,
    ),
    "ivf_flat": MessageToDict(
        VectorIndexParameter(
            ivf_flat_parameter=CreateIvfFlatParam(
                dimension=None, metric_type=None, ncentroids=256
            ),
            vector_index_type=VECTOR_INDEX_TYPE_IVF_FLAT,
        ),
        including_default_value_fields=True,
    ),
    "ivf_pq": MessageToDict(
        VectorIndexParameter(
            ivf_pq_parameter=CreateIvfPqParam(
                dimension=None,
                metric_type=None,
                ncentroids=256,
                nsubvector=8,
                bucket_init_size=1000,
                bucket_max_size=128000
            ),
            vector_index_type=VECTOR_INDEX_TYPE_IVF_PQ,
        ),
        including_default_value_fields=True,
    ),
    "hnsw": MessageToDict(
        VectorIndexParameter(
            hnsw_parameter=CreateHnswParam(
                dimension=None,
                efConstruction=200,
                max_elements=50000,
                metric_type=None,
                nlinks=32,
            ),
            vector_index_type=VECTOR_INDEX_TYPE_HNSW,
        ),
        including_default_value_fields=True,
    ),
    "diskann": MessageToDict(
        VectorIndexParameter(
            diskann_parameter=CreateDiskAnnParam(dimension=None, metric_type=None),
            vector_index_type=VECTOR_INDEX_TYPE_DISKANN,
        ),
        including_default_value_fields=True,
    ),
}
