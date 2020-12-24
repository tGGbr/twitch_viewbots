"""This module implements several proxy stratagies."""
import asyncio
import logging
import re
import secrets
import string
from typing import Dict, List, Optional

from . import http_client as hc
from . import proxies

logger = logging.getLogger(__name__)


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
        username: Optional[str] = None,
        password: Optional[str] = None,
        ip: Optional[str] = None,
    ):
        """Implement constructor."""
        self.prot: str = prototype
        self.user: Optional[str] = username
        self.pswd: Optional[str] = password
        self.host: str = hostname
        self.port: int = port
        self.ip: Optional[str] = ip

    @property
    def url(self):
        """Return the proxy url."""
        if (self.user and self.pswd) is None:
            return f"{self.prot}://{self.host}:{self.port}"
        return f"{self.prot}://{self.user}:{self.pswd}@{self.host}:{self.port}"

    @property
    def tested(self) -> bool:
        """Return boolean if proxy was tested."""
        return self.ip is not None

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
        if self.ip:
            return f"Proxy({self.url}, {self.ip})"
        return f"Proxy({self.url})"

    def __repr__(self):
        """Change the repr() format to show the proxy url."""
        return self.__str__()

    def __eq__(self, other):
        """Check if the ips are equal."""
        return self.ip == other.ip

    def __hash__(self):
        """Define the hash of a Proxy."""
        return hash(self.ip)


class ProxyBase:
    """This is the base class for all proxy classes."""

    def __init__(self):
        """Implement constructor."""
        self.proxy_list: List[Proxy] = []
        self.config: Dict[str, Optional[str, int]] = {}


class ProxyTor(ProxyBase):
    """This class implements proxies from Tor."""

    def __init__(
        self,
        n_connections: int = 10,
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

    def _proxy_list_gen(self):
        """Generate proxy urls with random credentials."""
        rnd_str = self.__class__._random_str_gen
        self.proxy_list = [
            Proxy.from_url(
                f"socks5://{rnd_str()}:{rnd_str()}@{self.host}:{self.port}")
            for _ in range(self.n_conn)
        ]

    async def _test_proxies(self) -> None:
        """Test if proxies in proxy_list are working and remove duplicates."""
        semaphore = asyncio.Semaphore(10)

        async def test_proxy(proxy: proxies.Proxy) -> Proxy:
            async with semaphore:
                async with hc.Http(proxy_url=proxy.url) as s:
                    async with s.get("https://api.ipify.org?format=json") as r:
                        r_json = await r.json()
            proxy.ip = r_json.get("ip")
            logger.debug(f"Tested {proxy}")
            return proxy

        res = await asyncio.gather(*[test_proxy(p) for p in self.proxy_list])
        self.proxy_list = list(set(res))
        self.n_conn = len(self.proxy_list)

    def create(self) -> List[Proxy]:
        """Create a untested proxy list."""
        return self._proxy_list_gen()

    def test(self) -> None:
        """Test proxies and discard not uniques."""
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(self._test_proxies())
        finally:
            loop.close()

    def run(self):
        """Create and test a proxy list."""
        self.create()
        self.test()


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
    logging.basicConfig(level=logging.DEBUG)
    tor_obj = ProxyTor(n_connections=250)
    tor_obj.run()
    logger.debug(tor_obj.n_conn)
