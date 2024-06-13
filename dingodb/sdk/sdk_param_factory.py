#!/usr/bin/python3

from  dingosdk import dingo_store


class SDKParamFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_flat_param(index_type: str, flat_param_dict: dict) -> dingo_store.FlatParam:
        assert index_type == "flat"

        return dingo_store.FlatParam(
            flat_param_dict["dimension"], flat_param_dict["metricType"]
        )

    @staticmethod
    def create_ivf_flat_param(
        index_type: str, ivf_flat_param_dict: dict
    ) -> dingo_store.IvfFlatParam:
        assert index_type == "ivf_flat"

        param = dingo_store.IvfFlatParam(
            ivf_flat_param_dict["dimension"],
            ivf_flat_param_dict["metricType"],
        )
        param.ncentroids = ivf_flat_param_dict["ncentroids"]

        return param

    @staticmethod
    def create_ivf_pq_param(
        index_type: str, ivf_pq_param_dict: dict
    ) -> dingo_store.IvfPqParam:
        assert index_type == "ivf_pq"

        param = dingo_store.IvfPqParam(
            ivf_pq_param_dict["dimension"],
            ivf_pq_param_dict["metricType"],
        )
        param.ncentroids = ivf_pq_param_dict["ncentroids"]
        param.nsubvector = ivf_pq_param_dict["nsubvector"]
        param.bucket_init_size = ivf_pq_param_dict["bucketInitSize"]
        param.bucket_max_size = ivf_pq_param_dict["bucketMaxSize"]
        param.nbits_per_idx = ivf_pq_param_dict["nbitsPerIdx"]

        return param

    @staticmethod
    def create_hnsw_param(index_type: str, hnsw_param_dict: dict) -> dingo_store.HnswParam:
        assert index_type == "hnsw"

        param = dingo_store.HnswParam(
            hnsw_param_dict["dimension"],
            hnsw_param_dict["metricType"],
            hnsw_param_dict["maxElements"],
        )
        param.ef_construction = hnsw_param_dict["efConstruction"]
        param.nlinks = hnsw_param_dict["nlinks"]

        return param

    @staticmethod
    def create_diskann_param(
        index_type: str, diskann_param_dict: dict
    ) -> dingo_store.DiskAnnParam:
        assert index_type == "hnsw"
        raise Exception(f"index_type diskann is not support now")

    @staticmethod
    def create_brute_param(
        index_type: str, brute_param_dict: dict
    ) -> dingo_store.BruteForceParam:
        assert index_type == "brute"

        return dingo_store.BruteForceParam(
            brute_param_dict["dimension"],
            brute_param_dict["metricType"],
        )
