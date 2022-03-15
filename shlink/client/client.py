from typing import Optional

from aiohttp import ClientSession

from shlink import __version__
from shlink.client.error import ShlinkError
from shlink.client.http.domain import Domain
from shlink.client.http.health import Health
from shlink.client.http.integration import Integration
from shlink.client.http.short_urls import ShortURLs
from shlink.client.http.tags import Tags
from shlink.client.http.visits import Visits


class Shlink(Domain, Health, Integration, ShortURLs, Tags, Visits):
    def __init__(self, url: str, api_key: str):
        self.url = url
        if self.url[-1] != "/":
            self.url = self.url + "/"
        self.api_url = self.url + "rest/v2"
        self.api_key = api_key

        headers = {
            "Accept": "application/problem+json",
            "X-Api-Key": self.api_key,
            "User-Agent": f"shlink-py/{__version__}",
        }
        self._session = ClientSession()
        self._session.headers = headers

    def __del__(self):
        self._session.close()

    async def _request(
        self, endpoint: str, data: Optional[dict] = None, params: Optional[dict] = None, method: str = "GET"
    ) -> Optional[dict]:
        """
        Make an API request

        Args:
            endpoint: Endpoint to request
            data: Optional data payload
            method: Request type, oneof DELETE, GET, PATCH, POST, PUT

        Return:
            Response or None if there's no API response

        Raises:
            ValueError with incorrect request types and data mismatches
            ShlinkError with `ShlinkError.data` being the error object
        """
        if method not in ["DELETE", "GET", "PATCH", "POST", "PUT"]:
            raise ValueError("Invalid request type")
        if method in ["PATCH", "POST", "PUT"] and not data:
            raise ValueError("Data required for this request type")

        endpoint = self.api_url + endpoint
        response = await self._session.request(method=method, url=endpoint, data=data, params=params)
        if not (200 <= response.status_code < 400):
            raise ShlinkError(data=await response.json())

        try:
            return await response.json()
        except Exception:  # The endpoint doesn't return JSON
            return None
