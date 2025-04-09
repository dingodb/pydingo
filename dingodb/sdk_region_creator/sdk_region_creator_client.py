import dingosdk

from dingodb.sdk_client import SDKClient


from .sdk_region_creator_param import (
    CreateRegionParam,
)


class RegionCreatorClient:
    """
    RegionCreatorClient is a wrapper for Dingodb SDK Region Creator client.
    """

    def __init__(self, client: SDKClient):
        """
        __init__ init Client

        Args:
            client: SDKClient
        """
        self.client = client.dingosdk_client

        s, self.region_creator_client = self.client.NewRegionCreator()
        if not s.ok():
            raise RuntimeError(f"NewRegionCreator failed, err: {s.ToString()}")

    def create_region(self, param: CreateRegionParam) -> int:
        """
        create_region create region

        Args:
            param(CreateRegionParam): create region param

        Return:
            int: region id
        """

        self.region_creator_client.SetRegionName(param.region_name)
        self.region_creator_client.SetRange(param.start_key, param.end_key)
        self.region_creator_client.SetReplicaNum(param.replicas)
        self.region_creator_client.SetEngineType(param.engine_type)

        s, region_id = self.region_creator_client.Create(param.region_id)
        if s.ok():
            return region_id
        else:
            raise RuntimeError(f"CreateRegion failed, err: {s.ToString()}")

    def drop_region(self, region_id: int):
        """
        drop_region drop region

        Args:
            region_id: region id
        """
        s = self.client.DropRegion(region_id)
        if not s.ok():
            raise RuntimeError(f"DropRegion failed, err: {s.ToString()}")

    def create_region_id(self, count: int) -> list[int]:
        """
        create_region_id create region id

        Args:
            region_id: region id

        Return:
            list[int]: list of region ids
        """

        s, region_ids = self.region_creator_client.CreateRegionId(count)
        if not s.ok():
            raise RuntimeError(f"CreateRegionId failed, err: {s.ToString()}")
        return region_ids
