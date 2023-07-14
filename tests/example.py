#!/usr/bin/python3

import pydingo
import numpy as np

x = pydingo.DingoDB("user", "password", ["172.20.3.20:13000"])


# index_name
# dimension
# index_type "flat"/"ivf_flat"/"ivf_pq"/"hnsw"/"diskann"
# metric_type "euclidean"/"product"/None
# replicas
# index_config = {"efConstruction":n, "maxElements":n, "nlinks":n}
# metadata_config = {}
# partition_rule = {}
b1 = x.create_index("test", 6, "hnsw", "euclidean", 0, {}, {}, {})
print(b1)
# b1 = True
# RuntimeError

# index_name
b2 = x.describe_index_info("test")
print(b2)
# b2 = {'name': 'test', 'version': 0, 'replica': 0, 'autoIncrement': 1, 'indexPartition': None, 'indexParameter': {'indexType': 'INDEX_TYPE_VECTOR', 'vectorIndexParameter': {'vectorIndexType': 'VECTOR_INDEX_TYPE_HNSW', 'flatParam': None, 'ivfFlatParam': None, 'ivfPqParam': None, 'hnswParam': {'dimension': 6, 'metricType': 'METRIC_TYPE_L2', 'efConstruction': 200, 'maxElements': 50000, 'nlinks': 32}, 'diskAnnParam': None}}}
# RuntimeError

# 构建训练数据和查询数据
d = 6                           # dimension
nb = 4                      # database size
np.random.seed(1234)             # make reproducible
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000.

ids = [1, 2, 3, 4]
datas = [{"a1": "b1"}, {"a2": "b2"}, {"a3": "b3"}, {"a4": "b4"}]
vectors = xb.tolist()
# vectors = [[321.213,3213.22,1,0,32.3,0.5],[3212.213,32513.22,1,50,32.3,0.5],[321.26413,32143.22,14536,0,32.345,0.5],[334534321.213454,3213453453.22,1,0,3265.3,0.5]]
# index_name
# ids = [id1, id2, id3]
# datas = [{data1key:data1value}, {data2key:data2value}, {data3key:data3value}]
# vectors = [[float1_1, float1_2, float1_3], [float2_1, float2_2, float2_3], [float3_1, float3_2, float3_3]]
b3 = x.vector_add("test", datas, vectors, ids)
print(b3)
# b3 = [{'id': 1, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.19151945, 0.62210876, 0.43772775, 0.7853586, 0.77997583, 0.2725926], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}}, {'id': 2, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.27746424, 0.8018722, 0.95813936, 0.87593263, 0.35781726, 0.5009951], 'binaryValues': []}, 'scalarData': {'a2': {'fieldType': 'STRING', 'fields': [{'data': 'b2'}]}}}, {'id': 3, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.6854629, 0.71270204, 0.37025076, 0.5611962, 0.50308317, 0.013768449], 'binaryValues': []}, 'scalarData': {'a3': {'fieldType': 'STRING', 'fields': [{'data': 'b3'}]}}}, {'id': 4, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.77582663, 0.8826412, 0.364886, 0.6153962, 0.07538124, 0.368824], 'binaryValues': []}, 'scalarData': {'a4': {'fieldType': 'STRING', 'fields': [{'data': 'b4'}]}}}]
# RuntimeError

# index_name
# xq = [float1, float2, float3]
# topk
# search_paras = []
b4 = x.vector_search("test", vectors[0])
print(b4)
# b4 = {'vectorWithDistances': [{'id': 1, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.19151945, 0.62210876, 0.43772775, 0.7853586, 0.77997583, 0.2725926], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}, 'distance': 0.0}, {'id': 3, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.6854629, 0.71270204, 0.37025076, 0.5611962, 0.50308317, 0.013768449], 'binaryValues': []}, 'scalarData': {'a3': {'fieldType': 'STRING', 'fields': [{'data': 'b3'}]}}, 'distance': 0.4506487}, {'id': 2, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.27746424, 0.8018722, 0.95813936, 0.87593263, 0.35781726, 0.5009951], 'binaryValues': []}, 'scalarData': {'a2': {'fieldType': 'STRING', 'fields': [{'data': 'b2'}]}}, 'distance': 0.5491189}, {'id': 4, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.77582663, 0.8826412, 0.364886, 0.6153962, 0.07538124, 0.368824], 'binaryValues': []}, 'scalarData': {'a4': {'fieldType': 'STRING', 'fields': [{'data': 'b4'}]}}, 'distance': 0.9491992}]}
# RuntimeError

# index_name
# xq = [float1, float2, float3]
# topk
# data = {data1key:data1value}
# search_paras = []
b4 = x.vector_search("test", vectors[0], 10, {"meta_expr": {"a1": "b1"}})
print(b4) 
# b4 = {'vectorWithDistances': [{'id': 1, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.19151945, 0.62210876, 0.43772775, 0.7853586, 0.77997583, 0.2725926], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}, 'distance': 0.0}]}
# RuntimeError

b5 = x.get_index()
print(b5)
# b5 = ['test', 'zetyun_test1']
# RuntimeError

# index_name
# ids = [id1, id2, id3]
b6 = x.vector_get("test", [1, 2, 3])
print(b6)
# b6 = [{'id': 1, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.19151945, 0.62210876, 0.43772775, 0.7853586, 0.77997583, 0.2725926], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}}, {'id': 2, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.27746424, 0.8018722, 0.95813936, 0.87593263, 0.35781726, 0.5009951], 'binaryValues': []}, 'scalarData': {'a2': {'fieldType': 'STRING', 'fields': [{'data': 'b2'}]}}}, {'id': 3, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.6854629, 0.71270204, 0.37025076, 0.5611962, 0.50308317, 0.013768449], 'binaryValues': []}, 'scalarData': {'a3': {'fieldType': 'STRING', 'fields': [{'data': 'b3'}]}}}]
# RuntimeError

# index_name
b7 = x.get_max_index_row("test")
print(b7)
# b7 = id
# RuntimeError

# index_name
# ids = [id1, id2, id3]
b8 = x.vector_delete("test", [1, 2, 3])
print(b8)
# b8 = [True, True, True]
# RuntimeError

# index_name
# max_element
b9 = x.update_index_max_element("test", 50001)
print(b9)
# b9 = True
# RuntimeError
print(x.describe_index_info("test"))

# index_name
b10 = x.delete_index("test")
print(b10)
# b10 = True
# RuntimeError
