import unittest

from core.proxies import Proxy


class TestProxy(unittest.TestCase):

    def test_constructor_from_url(self):
        proxy_url = "socks5://username:password@localhost:9050"
        proxy = Proxy.from_url(proxy_url)
        self.assertEqual(proxy.prot, "socks5")
        self.assertEqual(proxy.user, "username")
        self.assertEqual(proxy.pswd, "password")
        self.assertEqual(proxy.host, "localhost")
        self.assertEqual(proxy.port, 9050)

    def test_constructor_from_url_without_username_or_password(self):
        proxy_url = "socks5://localhost:9050"
        proxy = Proxy.from_url(proxy_url)
        self.assertEqual(proxy.prot, "socks5")
        self.assertEqual(proxy.host, "localhost")
        self.assertEqual(proxy.port, 9050)


if __name__ == "__main__":
    unittest.main()
