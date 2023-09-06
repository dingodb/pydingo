# python-dingodb
The DingoDB python sdk

First, you have prepared the DingoDB environment, see the docs at https://github.com/dingodb/dingo-deploy.git

For more information about DingoDB, see the docs at https://dingodb.readthedocs.io/en/latest/


## How to Contribute

### 1. Compile

```
pip install -r requirements.txt
git submodule update --init --recursive
```

### 2. Release



## Usage

### Installation

1. Install from pypi

```shell
pip3 install dingodb
```

2. Install from Source

```shell
pip install git+https://github.com/dingodb/pydingo.git
```

### Basic API

#### Creating an index

The following example creates an index without a metadata configuration. 
```python
>>> import dingodb
>>> dingo_client = dingodb.DingoDB("user", "password", ["172.20.3.20:13000"])
>>> dingo_client.create_index("testdingo", 6, index_type="flat")
True
```
dingodb provides flexible indexing parameters.
```python
>>> help(dingo_client.create_index)
create_index(index_name, dimension, index_type='hnsw', metric_type='euclidean', replicas=3, index_config=None, metadata_config=None, partition_rule=None, auto_id=True)
```

#### Get index
The following example returns all indexes in your schema.
```python
>>> dingo_client.get_index()
['testdingo']
```

#### Get index info

The following example returns the info in specified index.
```python
>>> dingo_client.describe_index_info("testdingo")
{'name': 'testdingo', 'version': 0, 'replica': 3, 'autoIncrement': 1, 'indexParameter': {'indexType': 'INDEX_TYPE_VECTOR', 'vectorIndexParameter': {'vectorIndexType': 'VECTOR_INDEX_TYPE_FLAT', 'flatParam': {'dimension': 6, 'metricType': 'METRIC_TYPE_L2'}, 'ivfFlatParam': None, 'ivfPqParam': None, 'hnswParam': None, 'diskAnnParam': None}}}
```

#### Add vector

The following example add vector to database.
```python
>>> dingo_client.vector_add("testdingo", [{"a1":"b1", "aa1":"bb1"}, {"a1": "b1"}],[[0.19151945,0.62210876,0.43772775,0.7853586,0.77997583,0.2725926], [0.27746424078941345,0.801872193813324,0.9581393599510193,0.8759326338768005,0.35781726241111755,0.5009950995445251]])
[{'id': 1, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.19151945, 0.62210876, 0.43772775, 0.7853586, 0.77997583, 0.2725926], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}, 'aa1': {'fieldType': 'STRING', 'fields': [{'data': 'bb1'}]}}}, {'id': 2, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.27746424, 0.8018722, 0.95813936, 0.87593263, 0.35781726, 0.5009951], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}}]
```

#### Get MAX ID

you can use autoIncrement id, The following example get max id
```python
>>> dingo_client.get_max_index_row("testdingo")
2
```

#### Search Vector

The following example Basic Search without metata.
```python
>>> dingo_client.vector_search("testdingo", [[0.19151945,0.62210876,0.43772775,0.7853586,0.77997583,0.2725926]], 10)
[{'vectorWithDistances': [{'id': 1, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}, 'aa1': {'fieldType': 'STRING', 'fields': [{'data': 'bb1'}]}}, 'distance': 0.0}, {'id': 2, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}, 'distance': 0.5491189}]}]
```

The following example Search with metata.
```python
>>> dingo_client.vector_search("testdingo", [0.19151945,0.62210876,0.43772775,0.7853586,0.77997583,0.2725926],10, {"meta_expr": {"aa1": "bb1"}})
{'vectorWithDistances': [{'id': 1, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [], 'binaryValues': []}, 'scalarData': {'aa1': {'fieldType': 'STRING', 'fields': [{'data': 'bb1'}]}, 'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}, 'distance': 0.0}]}
```

#### Query vector with ids

The following example Query vector with ids.
```python
>>> dingo_client.vector_get("testdingo", [2])
[{'id': 2, 'vector': {'dimension': 6, 'valueType': 'FLOAT', 'floatValues': [0.27746424, 0.8018722, 0.95813936, 0.87593263, 0.35781726, 0.5009951], 'binaryValues': []}, 'scalarData': {'a1': {'fieldType': 'STRING', 'fields': [{'data': 'b1'}]}}}]
```

#### Detele vector with ids

The following example Detele vector with ids.
```python
>>> dingo_client.vector_delete("testdingo", [2])
[True]
```

#### Drop index

The following example Drop one index.
```python
>>> dingo_client.delete_index("testdingo")
True
```
