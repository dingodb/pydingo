from enum import Enum


class KVPair :
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def to_dict(self):
        return {"key": self.key, "value": self.value}
    

class KeyOpState :
    def __init__(self, key: str, state: bool):
        self.key = key
        self.state = state

    def to_dict(self):
        return {"key": self.key, "state": self.state}