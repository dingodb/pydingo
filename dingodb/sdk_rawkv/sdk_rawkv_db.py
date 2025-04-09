import dingosdk

from dingodb.sdk_client import SDKClient
from dingodb.sdk_rawkv.sdk_rawkv_client import RawKVClient


from dingodb.common.rawkv_rep import (
    KVPair,
    KeyOpState,
)


class SDKRawKVDingoDB:
    """
    SDKRawKVDingoDB is a wrapper for Dingodb SDK RawKV client.
    """

    def __init__(self, client: SDKClient):
        """
        __init__ init Client

        Args:
            client: SDKClient
        """
        self.client = RawKVClient(client)

    def rawkv_put(self, key: str, value: str):
        """
        rawkv_put put key and value

        Args:
            key: key
            value: value
        """
        return self.client.rawkv_put(key, value)

    def rawkv_batch_put(self, kvs: list[tuple[str, str]]):
        """
        rawkv_batch_put put key and value

        Args:
            kvs: key and value list
        """
        sdk_kvs = [dingosdk.KVPair(key=k, value=v) for k, v in kvs]
        return self.client.rawkv_batch_put(sdk_kvs)

    def rawkv_get(self, key: str) -> str:
        """
        rawkv_get get value by key

        Args:
            key: key

        Return:
            str: value
        """
        return self.client.rawkv_get(key)

    def rawkv_batch_get(self, keys: list[str]) -> list[KVPair]:
        """
        rawkv_batch_get get values by keys

        Args:
            keys: keys

        Return:
            list[KVPair]: list of key value pairs
        """
        return self.client.rawkv_batch_get(keys)

    def rawkv_put_if_absent(self, key: str, value: str) -> bool:
        """
        rawkv_put_if_absent put key and value if absent

        Args:
            key: key
            value: value

        Return:
            bool: true if put success, false if key already exists
        """
        return self.client.rawkv_put_if_absent(key, value)

    def rawkv_batch_put_if_absent(self, kvs: list[tuple[str, str]]) -> list[KeyOpState]:
        """
        rawkv_batch_put_if_absent put key and value if absent

        Args:
            kvs: key and value list

        Return:
            list[KeyOpState]: list of key operation states
        """
        sdk_kvs = [dingosdk.KVPair(key=k, value=v) for k, v in kvs]
        return self.client.rawkv_batch_put_if_absent(sdk_kvs)

    def rawkv_delete(self, key: str):
        """
        rawkv_delete delete key

        Args:
            key: key
        """
        return self.client.rawkv_delete(key)

    def rawkv_batch_delete(self, keys: list[str]):
        """
        rawkv_batch_delete delete keys

        Args:
            keys: keys
        """
        return self.client.rawkv_batch_delete(keys)

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
        return self.client.rawkv_delete_range(start_key, end_key, continuous)

    def rawkv_compare_and_set(self, key: str, value: str, expected_value: str) -> bool:
        """
        rawkv_compare_and_set compare and set key value

        Args:
            key: key
            value: value to compare if equal
            expected_value: expected value to set

        Return:
            bool: true if compare success and set expected_value
        """
        return self.client.rawkv_compare_and_set(key, value, expected_value)

    def rawkv_batch_compare_and_set(
        self, kvs: list[tuple[str, str, str]], expected_values: list[str]
    ) -> list[KeyOpState]:
        """
        rawkv_batch_compare_and_set batch compare and set key value

        Args:
            kvs: list of key value pairs to compare if equal
            expected_values: list of expected values to set

        Return:
            list[KeyOpState]: list of key operation states
        """
        sdk_kvs = [dingosdk.KVPair(key=k, value=v) for k, v in kvs]
        return self.client.rawkv_batch_compare_and_set(sdk_kvs, expected_values)

    def rawkv_scan(self, start_key: str, end_key: str, limit: int) -> list[KVPair]:
        """
        rawkv_scan scan key value pairs

        Args:
            start_key: start key
            end_key: end key
            limit: limit key count

        Return:
            list[KVPair]: list of key value pairs
        """
        return self.client.rawkv_scan(start_key, end_key, limit)
