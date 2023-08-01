import pytest
import numpy as np
from dingodb import DingoDB

test_config = {
    "flat_l2": ("flat", "euclidean", None, {"meta_expr": {"a1": "b1"}}), 
    "flat_ip": ("flat", "dotproduct", None, None), 
    "flat_cosine": ("flat", "cosine", None, None),
    "hnsw_l2": ("hnsw", "euclidean", {
                            "efConstruction": 100,
                            "maxElements": 50000,
                            "nlinks": 32
                        }, {"efSearch": 10}), 
    "hnsw_ip": ("hnsw", "dotproduct", {
                            "efConstruction": 300,
                            "maxElements": 60000,
                            "nlinks": 64
                        }, {"efSearch": 20}),
    "hnsw_cosine": ("hnsw", "cosine", {
                            "efConstruction": 300,
                            "maxElements": 60000,
                            "nlinks": 64
                        }, {"efSearch": 20})
}


class TestIndex:
    # make dataset
    d = 6                           # dimension
    nb = 4                      # database size
    np.random.seed(1234)             # make reproducible
    xb = np.random.random((nb, d)).astype('float32')
    xb[:, 0] += np.arange(nb) / 1000.
    xb = xb.tolist()
    ids = [1, 2, 3, 4]
    datas = [{"a1": "b1"}, {"a2": "b2"}, {"a3": "b3"}, {"a4": "b4"}]
    host = ["172.20.3.20:13000"]
    db_client = DingoDB("user", "passwd", host)
    
    @pytest.mark.run(order=1)
    def test_create_index(self):
        for index_name, value in test_config.items():
            if index_name in self.db_client.get_index():
                self.db_client.delete_index(index_name)
            assert self.db_client.create_index(index_name, self.d, value[0], value[1], index_config=value[2]) is True
    
    @pytest.mark.run(order=2)
    def test_describe_index_info(self):
        for index_name in test_config.keys():
            describe_info = self.db_client.describe_index_info(index_name)
            assert isinstance(describe_info, dict)
    
    @pytest.mark.run(order=3)
    def test_add_index(self):
        for index_name in test_config.keys():
            self.db_client.vector_add(index_name, self.datas, self.xb)
    
    @pytest.mark.run(order=4)
    def test_count(self):
        for index_name in test_config.keys():
            count = self.db_client.vector_count(index_name)
            assert count == self.nb
             
    @pytest.mark.run(order=5)
    def test_scan_index(self):
        for index_name in test_config.keys():
            scan_res = self.db_client.vector_scan(index_name, 1, 100)
            assert len(scan_res) == self.nb
    
    @pytest.mark.run(order=6)
    def test_get_max_index_row(self):
        for index_name in test_config.keys():
            max_id = self.db_client.get_max_index_row(index_name)
            assert max_id == self.nb
             
    @pytest.mark.run(order=7)
    def test_vector_search(self):
        for index_name, value in test_config.items():
            search_res = self.db_client.vector_search(index_name, self.xb[0], search_params=value[3])
            assert len(search_res) > 0
    
    @pytest.mark.run(order=8)
    def test_vector_get(self):
        for index_name in test_config.keys():
            get_data = self.db_client.vector_get(index_name, [1, 2, 3])
            assert len(get_data) == 3
    
    @pytest.mark.run(order=9)
    def test_vector_delete(self):
        for index_name in test_config.keys():
            self.db_client.vector_delete(index_name, [1, 2])
            vector_count = self.db_client.vector_count(index_name)
            assert vector_count == 2
    
    @pytest.mark.run(order=10)
    def test_delete_index(self):
        for index_name in test_config.keys():
            del_status = self.db_client.delete_index(index_name)
            assert del_status is True


if __name__ == "__main__":
    pytest.main()
