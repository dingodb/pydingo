import dingosdk


from dingodb.common.rawkv_rep import (
    KVPair,
    KeyOpState,
)

def sdk_kvpairs_to_kv_pairs(
    sdk_kv_pairs: list[dingosdk.KVPair]
) -> list[KVPair]:
    return [KVPair(key=x.key, value=x.value) for x in sdk_kv_pairs]

def sdk_keyops_to_keyops(
    sdk_key_ops: list[dingosdk.KeyOpState]
) -> list[KeyOpState]:
    return [
        KeyOpState(key=x.key, state=x.state) for x in sdk_key_ops
    ]