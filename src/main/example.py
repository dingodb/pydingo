#!/usr/bin/python3

import pydingo

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
# b1 = False

# index_name
b2 = x.describe_index_info("test")
print(b2)
# b2 = {'name': 'test', 'version': 0, 'replica': 0, 'autoIncrement': 1, 'indexParameter': {'indexType': 'INDEX_TYPE_VECTOR', 'vectorIndexParameter': {'vectorIndexType': 'VECTOR_INDEX_TYPE_HNSW', 'flatParam': None, 'ivfFlatParam': None, 'ivfPqParam': None, 'hnswParam': {'dimension': 6, 'metricType': 'METRIC_TYPE_L2', 'efConstruction': 200, 'maxElements': 10000, 'nlinks': 32}, 'diskAnnParam': None}}}
# b2 = {'version': -1}

ids = [1,2,3,4]
datas = [{"a1":"b1"},{"a2":"b2"},{"a3":"b3"},{"a4":"b4"}]
vectors = [[321.213,3213.22,1,0,32.3,0.5],[3212.213,32513.22,1,50,32.3,0.5],[321.26413,32143.22,14536,0,32.345,0.5],[334534321.213454,3213453453.22,1,0,3265.3,0.5]]
# index_name
# ids = [id1, id2, id3]
# datas = [{data1key:data1value}, {data2key:data2value}, {data3key:data3value}]
# vectors = [[float1_1, float1_2, float1_3], [float2_1, float2_2, float2_3], [float3_1, float3_2, float3_3]]
b3 = x.vector_add("test", ids, datas, vectors)
print(b3)
# b3 = [{'id': 1, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [321.213, 3213.22, 1.0, 0.0, 32.3, 0.5], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}}, {'id': 2, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [3212.213, 32513.22, 1.0, 50.0, 32.3, 0.5], 'binaryValues': []}, 'scalarData': {'a2': {'fieldType': 'STRING', 'fields': [{'data': 'b2'}]}}}, {'id': 3, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [321.26413, 32143.22, 14536.0, 0.0, 32.345, 0.5], 'binaryValues': []}, 'scalarData': {'a3': {'fieldType': 'STRING', 'fields': [{'data': 'b3'}]}}}, {'id': 4, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [334534336.0, 3213453570.0, 1.0, 0.0, 3265.3, 0.5], 'binaryValues': []}, 'scalarData': {'a4': {'fieldType': 'STRING', 'fields': [{'data': 'b4'}]}}}]

# index_name
# xq = [float1, float2, float3]
# search_paras = []
# topk
b4 = x.vector_search("test", vectors[0], [], 10)
print(b4)
# b4 = {'vectorWithDistances': [{'id': 1, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [321.213, 3213.22, 1.0, 0.0, 32.3, 0.5], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}, 'distance': 0.0}]}
# b4 = []

b5 = x.get_index()
print(b5)
# b5 = ['test', 'zetyun_test1']
# b5 = []

# index_name
# ids = [id1, id2, id3]
b6 = x.vector_get("test", [1,2,3])
print(b6)
# b6 = [{'id': 1, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [321.213, 3213.22, 1.0, 0.0, 32.3, 0.5], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}}, {'id': 2, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [3212.213, 32513.22, 1.0, 50.0, 32.3, 0.5], 'binaryValues': []}, 'scalarData': {'a2': {'fieldType': 'STRING', 'fields': [{'data': 'b2'}]}}}, {'id': 3, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [321.26413, 32143.22, 14536.0, 0.0, 32.345, 0.5], 'binaryValues': []}, 'scalarData': {'a3': {'fieldType': 'STRING', 'fields': [{'data': 'b3'}]}}}]
# b6 = []

# index_name
b7 = x.get_max_index_row("test")
print(b7)
# b7 = id
# b7 = -1

# index_name
# ids = [id1, id2, id3]
b8 = x.vector_delete("test", [1,2,3])
print(b8)
# b8 = [True, True, True]
# b8 = []

# index_name
b9 = x.delete_index("test")
print(b9)
# b9 = True
# b9 = False