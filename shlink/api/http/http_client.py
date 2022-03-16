from typing import Any, Dict, Optional, TYPE_CHECKING

from aiohttp import ClientSession

from shlink.api.http.http_requests import (
    Domain,
    Health,
    Integration,
    ShortURLs,
    Tags,
    Visits,
)
from shlink.client.const import __version__
from shlink.client.error import ShlinkError

if TYPE_CHECKING:
    from shlink.client.client import Shlink

__all__ = ["HTTPClient"]


class HTTPClient(Domain, Health, Integration, ShortURLs, Tags, Visits):
    def __init__(self, api_key: str, url: str, client: "Shlink"):
        self._api_key = api_key
        self._client = client
        self._default_headers = {
            "Accept": "application/problem+json",
            "X-Api-Key": self._api_key,
            "User-Agent": f"shlink-py/{__version__}",
        }
        self.base_url = url
        if self.base_url[-1] == "/":
            self.base_url = self.base_url[:-1]
        self.api_path = "/rest/v2"
        self.__session = ClientSession(
            headers=self._default_headers, base_url=self.base_url
        )

    async def request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
    ) -> Optional[Dict[str, Any]]:
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

        endpoint = self.api_path + endpoint
        response = await self.__session.request(
            method=method, url=endpoint, data=data, params=params
        )
        if not (200 <= response.status < 400):
            raise ShlinkError(data=await response.json())

        try:
            return await response.json()
        except Exception:  # The endpoint doesn't return JSON
            return None

    def __del__(self):
        self.__session.close()
