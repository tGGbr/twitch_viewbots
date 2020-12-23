"""This module implements the bot."""
from typing import List

from . import proxies


class BotManager:
    """This class manages several Twitch viewbots."""

    def __init__(self, proxy_strat: proxies.ProxyBase):
        """Implement constructor."""
        self.proxies = proxy_strat.proxy_list
        self.config = proxy_strat.config
        self.bots: List[Bot] = []


class Bot:
    """This class implements a Twitch viewbot."""

    def __init__(self):
        """Implement constructor."""
        self.sessions: List[]
