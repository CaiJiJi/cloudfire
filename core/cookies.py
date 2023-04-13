from typing import List
from urllib.parse import urlparse

from redis.asyncio import Redis
from playwright.async_api import Cookie


class CookieManager:
    def __init__(self, redis: Redis = None) -> None:
        self.redis = redis
        self.cookie_map = {}

    async def add_cookies(self, url, cookies: List[Cookie]):
        if not self.redis:
            for cookie in cookies:
                domain = urlparse(url).netloc
                try:
                    self.cookie_map[domain][cookie["name"]] = cookie["value"]
                except KeyError:
                    self.cookie_map[domain] = {}
                    self.cookie_map[domain][cookie["name"]] = cookie["value"]

    async def get_cookies(self, domain: str):
        base = urlparse(domain).netloc
        if not self.redis:
            return self.cookie_map.get(base)

    async def get_all_cookies(self):
        if not self.redis:
            return self.cookie_map
