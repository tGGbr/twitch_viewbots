"""This module implements several proxy stratagies."""
from typing import Dict, List, Optional


class ProxyBase:
    """This is the base class for all proxy classes."""

    def __init__(self):
        """Implement constructor."""
        self.proxy_list: List[str] = []
        self.config: Dict[str, Optional[str, int]] = {}


class ProxyTor(ProxyBase):
    """This class implements proxies from Tor."""

    def __init__(self):
        """Implement constructor."""
        super().__init__()


class ProxyFile:
    """This class implements proxies from a file."""

    def __init__(self):
        """Implement constructor."""
        super().__init__()


class ProxyNordVPN:
    """This class implements proxies from NordVPN accounts."""

    def __init__(self):
        """Implement constructor."""
        super().__init__()


if __name__ == "__main__":
    obj_tor = ProxyTor()
