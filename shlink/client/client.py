from shlink.api.http.http_client import HTTPClient
from shlink.models.short import ShortUrlsView


class Shlink:
    def __init__(self, url: str, api_key: str):
        self.http = HTTPClient(api_key=api_key, url=url, client=self)

    async def fetch_short_urls(self) -> ShortUrlsView:
        """
        Fetch all short URLs.
        """
        return await self.http.get_short_urls()
