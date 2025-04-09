import dingosdk

from pydantic import BaseModel, validator


engine_types = {
    "LSM": dingosdk.EngineType.kLSM,
    "BTree": dingosdk.EngineType.kBTree,
    "XDPROCKS": dingosdk.EngineType.kXDPROCKS,
}


class CreateRegionParam(BaseModel):
    region_name: str
    start_key: str
    end_key: str
    region_id: int = -1
    replicas: int = 3
    engine_type: str = "LSM"

    @validator("replicas", always=True)
    def check_replicas(cls, value):
        if value < 0:
            raise Exception(f"{value} must >= 0")
        if value == 0:
            value = 3
        return value

    @validator("engine_type", always=True)
    def check_engine_type(cls, value):
        if value not in engine_types:
            raise Exception(f"{value} not in {engine_types.keys()}")
        return engine_types[value]
