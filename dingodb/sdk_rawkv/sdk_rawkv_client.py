import dingosdk

from dingodb.sdk_client import SDKClient
from .sdk_rawkv_adapter import sdk_kvpairs_to_kv_pairs, sdk_keyops_to_keyops

from dingodb.common.rawkv_rep import (
    KVPair,
    KeyOpState,
)


class RawKVClient:
    def __init__(self, client: SDKClient):
        """
        __init__ init Client

        Args:
            client: SDKClient
        """
        self.schema_id = 2
        self.client = client.dingosdk_client

        s, self.rawkv_client = self.client.NewRawKV()
        if not s.ok():
            raise RuntimeError(f"NewRawKV failed, err: {s.ToString()}")

    def rawkv_put(self, key: str, value: str):
        """
        put put key value

        Args:
            key: key
            value: value
        """
        s = self.rawkv_client.Put(key, value)
        if not s.ok():
            raise RuntimeError(f"Put failed, err: {s.ToString()}")

    def rawkv_batch_put(self, kvs: list[dingosdk.KVPair]):
        """
        batch_put batch put key value

        Args:
            kvs: list of key value pairs
        """
        s = self.rawkv_client.BatchPut(kvs)
        if not s.ok():
            raise RuntimeError(f"BatchPut failed, err: {s.ToString()}")

    def rawkv_get(self, key: str) -> str:
        """
        rawkv get key value

        Args:
            key: key

        Return:
            str: value
        """
        s, value = self.rawkv_client.Get(key)
        if not s.ok():
            raise RuntimeError(f"Get failed, err: {s.ToString()}")
        return value

    def rawkv_batch_get(self, keys: list[str]) -> list[KVPair]:
        """
        rawkv batch get key value

        Args:
            keys: list of keys

        Return:
            list[KVPair]: list of key value pairs
        """
        s, kvs = self.rawkv_client.BatchGet(keys)
        if not s.ok():
            raise RuntimeError(f"BatchGet failed, err: {s.ToString()}")
        return sdk_kvpairs_to_kv_pairs(kvs)

    def rawkv_put_if_absent(self, key: str, value: str) -> bool:
        """
        put_if_absent put key value if absent

        Args:
            key: key
            value: value

        Return:
            bool: true if put success, false if key already exists
        """
        s, state = self.rawkv_client.PutIfAbsent(key, value)
        if not s.ok():
            raise RuntimeError(f"PutIfAbsent failed, err: {s.ToString()}")
        return state

    def rawkv_batch_put_if_absent(self, kvs: list[dingosdk.KVPair]) -> list[KeyOpState]:
        """
        batch_put_if_absent batch put key value if absent

        Args:
            kvs: list of key value pairs

        Return:
            list[KeyOpState]: list of key operation states
        """
        s, states = self.rawkv_client.BatchPutIfAbsent(kvs)
        if not s.ok():
            raise RuntimeError(f"BatchPutIfAbsent failed, err: {s.ToString()}")
        return sdk_keyops_to_keyops(states)

    def rawkv_delete(self, key: str):
        """
        delete delete key

        Args:
            key: key
        """
        s = self.rawkv_client.Delete(key)
        if not s.ok():
            raise RuntimeError(f"Delete failed, err: {s.ToString()}")

    def rawkv_batch_delete(self, keys: list[str]):
        """
        batch_delete batch delete key

        Args:
            keys: list of keys
        """
        s = self.rawkv_client.BatchDelete(keys)
        if not s.ok():
            raise RuntimeError(f"BatchDelete failed, err: {s.ToString()}")

    def rawkv_delete_range(
        self, start_key: str, end_key: str, continuous: bool = False
    ):
        """
        delete_range delete range key

        Args:
            start_key: start key
            end_key: end key
            continuous: check region continuous

        """
        if continuous:
            s = self.rawkv_client.DeleteRange(start_key, end_key)
            if not s.ok():
                raise RuntimeError(f"DeleteRangeContinuous failed, err: {s.ToString()}")

        s = self.rawkv_client.DeleteRangeNonContinuous(start_key, end_key)
        if not s.ok():
            raise RuntimeError(f"DeleteRange failed, err: {s.ToString()}")

    def rawkv_compare_and_set(self, key: str, value: str, expected_value: str) -> bool:
        """
        compare_and_set compare and set key value

        Args:
            key: key
            value: value
            expected_value: expected value

        Return:
            bool: true if compare and set success, false if compare failed
        """
        s, state = self.rawkv_client.CompareAndSet(key, expected_value, value)
        if not s.ok():
            raise RuntimeError(f"CompareAndSet failed, err: {s.ToString()}")
        return state

    def rawkv_batch_compare_and_set(
        self, kvs: list[dingosdk.KVPair], expected_values: list[str]
    ) -> list[KeyOpState]:
        """
        batch_compare_and_set batch compare and set key value

        Args:
            kvs: list of key value pairs
            expected_values: list of expected values

        Return:
            list[KeyOpState]: list of key operation states
        """
        s, states = self.rawkv_client.BatchCompareAndSet(kvs, expected_values)
        if not s.ok():
            raise RuntimeError(f"BatchCompareAndSet failed, err: {s.ToString()}")
        return sdk_keyops_to_keyops(states)

    def rawkv_scan(
        self,
        start_key: str,
        end_key: str,
        limit: int,
    ) -> list[KVPair]:
        """
        scan scan key value

        Args:
            start_key: start key
            end_key: end key
            limit: limit key count

        Return:
            list[KVPair]: list of key value pairs
        """
        s, kvs = self.rawkv_client.Scan(start_key, end_key, limit)
        if not s.ok():
            raise RuntimeError(f"Scan failed, err: {s.ToString()}")
        return sdk_kvpairs_to_kv_pairs(kvs)
