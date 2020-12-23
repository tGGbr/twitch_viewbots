"""This module implements the bot."""
import asyncio
from typing import List, Optional

from . import http_client as hc
from . import proxies


class BotManager:
    """This class manages several Twitch viewbots."""

    def __init__(self,
                 proxy_strat: proxies.ProxyBase,
                 loop: asyncio.AbstractEventLoop = None):
        """Implement constructor."""
        self.loop = loop or asyncio.get_event_loop()
        self.proxy_url_list = proxy_strat.proxy_list
        self.config = proxy_strat.config
        self.bots: List[Bot] = []

    async def main(self):
        """Run main logic."""
        self.bots = [Bot(p_url) for p_url in self.proxy_url_list]
        await asyncio.gather(*[b.start() for b in self.bots])
        await asyncio.gather(*[b.close() for b in self.bots])

    def run(self):
        """Run main loop."""
        try:
            self.loop.run_until_complete(self.main())

        finally:
            self.loop.close()


class Bot:
    """This class implements a Twitch viewbot."""

    def __init__(self, proxy_url: Optional[str], n_sessions: int = 1):
        """Implement constructor."""
        self.n_sessions: int = n_sessions
        self.sessions: List[hc.Http] = []

    async def start(self):
        """Run when bot starts up."""
        self.sessions = [hc.Http() for _ in range(self.n_sessions)]

    async def close(self):
        """Run when bot stops."""
        await asyncio.gather(*[s.close() for s in self.sessions if s])


if __name__ == "__main__":
    """Basic testing"""
    p_strat = proxies.ProxyTor()
    p_strat.proxy_list = [None] * 10
    manager = BotManager(proxy_strat=p_strat)
    manager.run()
