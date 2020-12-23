"""This module implements the http interface."""
import asyncio
from typing import Optional

import aiohttp
from aiohttp_socks import ProxyConnector


class Http(aiohttp.ClientSession):
    """This class extends the ClientSession class from aiohttp."""

    def __init__(self, proxy_url: Optional[str] = None):
        """Implement constructor."""
        connector = ProxyConnector.from_url(proxy_url) if proxy_url else None
        super().__init__(connector=connector)


if __name__ == "__main__":
    """Basic testing"""

    async def run():
        """Async Test Function."""
        async with Http() as s:
            async with s.get("https://google.com") as r:
                print(await r.text())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
