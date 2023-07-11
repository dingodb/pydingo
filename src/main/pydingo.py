#!/usr/bin/python3

import requests
import json

class DingoDB:
    user = ""
    password = ""
    host = []
    headers = {"Content-Type":"application/json"}
    requestProto = "http://"
    indexApi = "/index/api/dingo/"
    vectorApi = "/vector/api/dingo/"
    
    def __init__(self, user, password, host) -> None:
        self.user = user
        self.password = password
        self.host = host

    def describe_index_info(self, index_name):
        req = requests.get(self.requestProto+self.host[0]+self.indexApi+index_name, headers = self.headers)
        if req.status_code == 200:
            return json.loads(req.content)
        return {"version":-1}

    def create_index(self, index_name, dimension, index_type="hnsw", metric_type="euclidean", replicas=3, index_config=None, metadata_config=None, partition_rule=None) -> bool:
        efConstruction = 200
        maxElements = 10000
        
        if index_config != None and index_config.get("efConstruction") != None :
            efConstruction = index_config.get("efConstruction")
        if index_config != None and index_config.get("maxElements") != None :
            maxElements = index_config.get("maxElements")
        if index_config != None and index_config.get("nlinks") != None :
            nlinks = index_config.get("nlinks")
            if nlinks <= 0:
                nlinks = 32
        else :
            nlinks = 32
        
        partitionRule = {}
        if partitionRule != None :
            partitionRule = partition_rule
        
        if metric_type == "euclidean" :
            metric_type = "METRIC_TYPE_L2"
        elif metric_type == "product" :
            metric_type = "METRIC_TYPE_INNER_PRODUCT"
        elif metric_type == None :
            metric_type = "METRIC_TYPE_NONE"

        vectorIndexParameter = {}
        if index_type == "flat" :
            vectorIndexParameter = {
                "flatParam": {
                    "dimension": 0
                },
                "vectorIndexType": "VECTOR_INDEX_TYPE_FLAT"
            }
        elif index_type == "ivf_flat" :
            vectorIndexParameter = {
                "ivfFlatParam": {
                    "dimension": 0,
                    "metricType": metric_type,
                    "ncentroids": 0
                },
                "vectorIndexType": "VECTOR_INDEX_TYPE_IVF_FLAT"
            }
        elif index_type == "ivf_pq" :
            vectorIndexParameter = {
                "ivfPqParam": {
                    "bucketInitSize": 0,
                    "bucketMaxSize": 0,
                    "dimension": 0,
                    "metricType": metric_type,
                    "ncentroids": 0,
                    "nsubvector": 0
                },
                "vectorIndexType": "VECTOR_INDEX_TYPE_IVF_PQ"
            }
        elif index_type == "hnsw" :
            vectorIndexParameter = {
                "hnswParam": {
                            "dimension": dimension,
                            "efConstruction": efConstruction,
                            "maxElements": maxElements,
                            "metricType": metric_type,
                            "nlinks": nlinks
                        },
                "vectorIndexType": "VECTOR_INDEX_TYPE_HNSW"
            }
        elif index_type == "diskann" :
            vectorIndexParameter = {
                "diskAnnParam": {
                    "dimension": 0,
                    "metricType": metric_type
                },
                "vectorIndexType": "VECTOR_INDEX_TYPE_DISKANN"
            }

        indexDefinition = {
  			"autoIncrement": 1,
            "isAutoIncrement": "true",
  			"indexParameter": {
                "indexType": "INDEX_TYPE_VECTOR",
                "vectorIndexParameter": vectorIndexParameter
		    },
            "name": index_name,
            "partitionRule": partitionRule,
            "replica": replicas,
            "version": 0
		}

        req = requests.put(self.requestProto+self.host[0]+self.indexApi, headers = self.headers, data=json.dumps(indexDefinition))
        if req.status_code == 200 :
            return True
        return False

    def delete_index(self, indexName) -> bool:
        req = requests.delete(self.requestProto+self.host[0]+self.indexApi+indexName)
        if req.status_code == 200 :
            return True
        return False

    def vector_add(self, index_name, datas, vectors, ids=None) -> bool:
        i = 0
        records = []
        scalarData = {}
        vector = {}
        for v in vectors :
            scalarData = dict((keys, {"fieldType": "STRING", "fields":[
	    {"data": values}]}) for keys,values in datas[i].items())
		
            vector = {
                    "binaryValues":[],
                    "dimension":len(v),
                    "floatValues":v,
                    "valueType":"FLOAT"
            }
            if ids==None or len(ids) != len(vectors) :
                record = {
                    "scalarData" : scalarData,
                    "vector" : vector
                }
            else :
                record = {
                    "id" : ids[i],
                    "scalarData" : scalarData,
                    "vector" : vector
                }
            i = i + 1
            records.append(record) 

        jsonstr = json.dumps(records)
        req = requests.put(self.requestProto+self.host[0]+self.vectorApi+index_name, headers = self.headers, data=jsonstr)
        if req.status_code == 200 :
            records = json.loads(req.content)
            return records
        return []

    def get_index(self):
        req = requests.get(self.requestProto+self.host[0]+self.indexApi, headers = self.headers)
        if req.status_code == 200 :
            indics = json.loads(req.content)
            return indics
        return []

    def get_max_index_row(self, index_name):
        req = requests.get(self.requestProto+self.host[0]+self.vectorApi+index_name+"/id?isGetMin=false", headers = self.headers)
        if req.status_code == 200 :
            id = json.loads(req.content)
            return id
        return -1

    def vector_search(self, index_name, xq, search_params, topk) -> bool:
        q = {
            "parameter":{
                "search": {
                    "hnswParam": {
                        "efSearch": 0
                    }
                },
                "selectedKeys":[],
                "topN":topk,
                "withScalarData": "true",
                "withoutVectorData": "false"
			},
            "vector":{
                "id":1,
                "scalarData":{},
                "vector":{
                    "binaryValues":[],
                    "dimension":len(xq),
                    "floatValues":xq,
                    "valueType":"FLOAT"
				}
			}
		}
        
        jsonstr = json.dumps(q)
        req = requests.post(self.requestProto+self.host[0]+self.vectorApi+index_name, headers = self.headers, data=jsonstr)
        if req.status_code == 200 :
            records = json.loads(req.content)
            return records
        return []
    
    def vector_get(self, index_name, ids) :
        q = {
            "ids": ids,
            "keys": [],
            "withScalarData": "true",
            "withoutVectorData": "false"
        }
        jsonstr = json.dumps(q)
        req = requests.post(self.requestProto+self.host[0]+self.vectorApi+index_name+"/get", headers = self.headers, data=jsonstr)
        if req.status_code == 200 :
            records = json.loads(req.content)
            return records
        return []

    def vector_delete(self, index_name, ids) :
        jsonstr = json.dumps(ids)
        req = requests.delete(self.requestProto+self.host[0]+self.vectorApi+index_name, headers = self.headers, data=jsonstr)
        if req.status_code == 200 :
            return json.loads(req.content)
        return []
