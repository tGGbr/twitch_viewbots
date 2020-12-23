"""This module implements several proxy stratagies."""
import re
import secrets
import string
from typing import Dict, List, Optional

from . import http_client as hc


class ProxyWrongFormatException(Exception):
    """Exception in case the proxy url format is wrong."""

    pass


class Proxy:
    """This class implements a proxy model."""

    PROXY_REGEX = re.compile(
        r"(\w*):\/\/(?:([\w\d-]*):([\d\w]*)@)?([\w\d]*):([\d]{2,7})")

    def __init__(
        self,
        prototype: str,
        hostname: str,
        port: int,
        username: Optional[str],
        password: Optional[str],
    ):
        """Implement constructor."""
        self.prot: str = prototype
        self.user: Optional[str] = username
        self.pswd: Optional[str] = password
        self.host: str = hostname
        self.port: int = port

    @property
    def url(self):
        """Return the proxy url."""
        if (self.user and self.pswd) is None:
            return f"{self.prot}://{self.host}:{self.port}"
        return f"{self.prot}://{self.user}:{self.pswd}@{self.host}:{self.port}"

    @classmethod
    def from_url(cls, url: str):
        """Implement constructor from a proxy string url."""
        match = cls.PROXY_REGEX.search(url)
        if match is not None:
            return cls(
                prototype=match.group(1),
                username=match.group(2),
                password=match.group(3),
                hostname=match.group(4),
                port=int(match.group(5)),
            )
        raise ProxyWrongFormatException

    def __str__(self):
        """Change the str() format to show the proxy url."""
        return f"Proxy({self.url})"


class ProxyBase:
    """This is the base class for all proxy classes."""

    def __init__(self):
        """Implement constructor."""
        self.proxy_list: List[Optional[str]] = []
        self.config: Dict[str, Optional[str, int]] = {}


class ProxyTor(ProxyBase):
    """This class implements proxies from Tor."""

    def __init__(
        self,
        n_connections: int = 200,
        tor_port: int = 9050,
        tor_host: str = "localhost",
    ):
        """Implement constructor."""
        super().__init__()
        self.n_conn: int = n_connections
        self.host: str = tor_host
        self.port: int = tor_port

    @staticmethod
    def _random_str_gen(n: int = 10) -> str:
        """Generate random string with size n."""
        pool = string.ascii_letters + string.digits
        return "".join([secrets.choice(pool) for _ in range(n)])

    def _proxy_url_gen(self) -> List[Optional[str]]:
        """Generate proxy urls with random credentials."""
        rnd_str = self.__class__._random_str_gen
        self.proxy_list = [
            f"socks5://{rnd_str()}:{rnd_str()}@{self.host}:{self.port}"
            for _ in range(self.n_conn)
        ]
        return self.proxy_list


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
