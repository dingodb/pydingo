import dingosdk


class SDKClient:
    def __init__(self, addrs: str):
        """
        Args:
            addrs (str): coordinator addrs, try to use like 127.0.0.1:22001,127.0.0.1:22002,127.0.0.1:22003

        Raises:
            RuntimeError: return error
        """
        self.addrs = addrs
        self.s, self.dingosdk_client = dingosdk.Client.BuildAndInitLog(addrs)

        if not self.s.ok():
            raise RuntimeError(f"dongo client build fail: {self.s.ToString()}")
