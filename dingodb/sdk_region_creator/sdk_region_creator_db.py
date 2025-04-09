import dingosdk


from dingodb.sdk_client import SDKClient
from dingodb.sdk_region_creator.sdk_region_creator_client import RegionCreatorClient

from .sdk_region_creator_param import (
    CreateRegionParam,
)


class SDKRegionCreatorDingoDB:
    """
    SDKRegionCreatorDingoDB is a wrapper for Dingodb SDK Region Creator client.
    """

    def __init__(self, client: SDKClient):
        """
        __init__ init Client

        Args:
            client: SDKClient
        """
        self.client = RegionCreatorClient(client)

    def create_region(
        self,
        region_name: str,
        start_key: str,
        end_key: str,
        region_id: int = -1,
        replicas: int = 3,
        engine_type="LSM",
    ) -> int:
        """
        create_region create region

        Args:
            region_name(str) : the name of region
            start_key(str) : start key
            end_key(str) : end key
            region_id(int, optional) : Defaults to -1 , means auto generate.
            replicas(int, optional) : dingoDB store replicas. Defaults to 3.
            engine_type(str, optional) : engine type, default is LSM
        """
        params = CreateRegionParam(
            region_name=region_name,
            start_key=start_key,
            end_key=end_key,
            region_id=region_id,
            replicas=replicas,
            engine_type=engine_type,
        )
        self.client.create_region(params)

    def drop_region(self, region_id: int):
        """
        drop_region drop region

        Args:
            region_id: region id
        """
        self.client.drop_region(region_id)

    def create_region_id(self, count: int) -> list[int]:
        """
        create_region_id create region id

        Args:
            count: create region id count
        """
        return self.client.create_region_id(count)
