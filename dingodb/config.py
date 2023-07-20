metric_type = {
    "euclidean": "METRIC_TYPE_L2",
    "product": "METRIC_TYPE_INNER_PRODUCT"
}


# proto
index_config = {
    "flat": {
                "flatParam": {
                    "dimension": None,
                    "metricType": None
                },
                "vectorIndexType": "VECTOR_INDEX_TYPE_FLAT"
            },
    "ivf_flat": {
                "ivfFlatParam": {
                    "dimension": None,
                    "metricType": None,
                    "ncentroids": 256
                },
                "vectorIndexType": "VECTOR_INDEX_TYPE_IVF_FLAT"
            },
    "ivf_pq": {
                "ivfPqParam": {
                    "bucketInitSize": 0,
                    "bucketMaxSize": 0,
                    "dimension": None,
                    "metricType": None,
                    "ncentroids": 256,
                    "nsubvector": 8
                },
                "vectorIndexType": "VECTOR_INDEX_TYPE_IVF_PQ"
            },
    "hnsw": {
                "hnswParam": {
                            "dimension": None,
                            "efConstruction": 200,
                            "maxElements": 50000,
                            "metricType": None,
                            "nlinks": 32
                        },
                "vectorIndexType": "VECTOR_INDEX_TYPE_HNSW"
            },
    "diskann": {
                "diskAnnParam": {
                    "dimension": None,
                    "metricType": None
                },
                "vectorIndexType": "VECTOR_INDEX_TYPE_DISKANN"
            }
}
