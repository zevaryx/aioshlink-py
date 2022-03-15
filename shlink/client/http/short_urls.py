from datetime import datetime
from json import dumps
from typing import List, Optional

from shlink.client.const import MISSING
from shlink.models.short import ShortUrlsView, ShortURL
from shlink.models.visits import VisitsView


class ShortURLs:
    async def get_short_urls(
        self,
        page: Optional[int] = 1,
        itemsPerPage: Optional[int] = 10,
        searchTerm: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tagsMode: Optional[str] = "any",
        orderBy: Optional[str] = None,
        startDate: Optional[datetime] = None,
        endDate: Optional[datetime] = None,
    ) -> ShortUrlsView:
        """
        Returns the list of short URLs.

        Args:
            page: The page to display. Defaults to 1
            itemsPerPage: The amount of items to return on every page. Defaults to all items
            searchTerm:
                A query used to filter results by searching for it on the
                longUrl and shortCode fields
            tags:
                A list of tags used to filter the result set.
                Only short URLs tagged with at least one of the provided tags will be returned.
            orderBy:
                The field from which you want to order the result.
            startDate: The date from which we want to get short URLs.
            endDate: The date until which we want to get short URLs.
        """
        if startDate:
            startDate = startDate.isoformat()
        if endDate:
            endDate = endDate.isoformat()
        payload = locals()
        del payload["self"]
        data = await self._request(endpoint="/short-urls", method="GET", data=dumps(payload))
        return ShortUrlsView.from_dict(data)

    async def create_short_url(
        self,
        longUrl: str,
        validSince: Optional[datetime] = None,
        validUntil: Optional[datetime] = None,
        maxVisits: Optional[int] = None,
        validateUrl: bool = True,
        tags: List[str] = [],
        title: Optional[str] = None,
        crawlable: bool = True,
        forwardQuery: bool = True,
        customSlug: Optional[str] = None,
        findIfExists: bool = True,
        domain: Optional[str] = None,
        shortCodeLength: Optional[int] = None,
    ) -> ShortURL:
        """
        Creates a new short URL.

        Args:
            longUrl: The long URL this short URL will redirect to
            validSince: The date from which this short code will be valid
            validUntil: The date until which this short code will be valid
            maxVisits: The maximum number of visits for this short code
            validateUrl:
                Tells if the long URL should or should not be validated as a reachable URL.
                If not provided, it will fall back to app-level config
            tags: The list of tags to set to the short URL
            title: A descriptive title of the short URL
            crawlable: Tells if this URL will be included as 'Allow' in Shlink's robots.txt
            forwardQuery:
                Tells if the query params should be forwarded from the short URL to the long one,
                as explained in the Shlink docs
            customSlug: A unique custom slug to be used instead of the generated short code
            findIfExists:
                Will force existing matching URL to be returned if found,
                instead of creating a new one
            domain: The domain to which the short URL will be attached
            shortCodeLength:
                The length for generated short code. It has to be at least 4 and defaults to 5.
                It will be ignored when customSlug is provided
        """
        payload = locals()
        del payload["self"]
        data = await self._request(endpoint="/short-urls", method="POST", params=payload)
        return ShortURL.from_dict(data)

    async def shorten(self, longUrl: str) -> ShortURL:
        """
        Creates a short URL in a single API call. Useful for third party integrations.

        Args:
            longURL: The long URL that this Short URL will redirect to
        """
        payload = {"apiKey": self.api_key, "longUrl": longUrl}
        data = await self._request(
            endpoint="/short-urls/shorten", method="GET", params=payload
        )
        return ShortURL.from_dict(data)

    async def get_short_url(self, shortCode: str) -> ShortURL:
        """
        Get the long URL behind a short URL's short code.

        Args:
            shortCode: The short code to resolve
        """
        data = await self._request(endpoint=f"/short-urls/{shortCode}", method="GET")
        return ShortURL.from_dict(data)

    async def delete_short_url(self, shortCode: str) -> None:
        """
        Deletes the short URL for provided short code.

        Args:
            shortCode: The short code to resolve
        """
        data = await self._request(endpoint=f"/short-urls/{shortCode}", method="DELETE")
        return data

    async def edit_short_url(
        self,
        shortCode: str,
        longUrl: Optional[str],
        validSince: Optional[datetime] = MISSING,
        validUntil: Optional[datetime] = MISSING,
        maxVisits: Optional[int] = MISSING,
        validateUrl: Optional[bool] = MISSING,
        tags: Optional[List[str]] = MISSING,
        title: Optional[str] = MISSING,
        crawlable: Optional[bool] = MISSING,
        forwardQuery: Optional[bool] = MISSING,
    ) -> ShortURL:
        """
        Update certain meta arguments from an existing short URL.

        Args:
            shortCode: The short code to edit
            longUrl: The long URL this short URL will redirect to
            validSince: The date from which this short code will be valid
            validUntil: The date until which this short code will be valid
            maxVisits: The maximum number of visits for this short code
            validateUrl:
                Tells if the long URL should or should not be validated as a reachable URL.
                If not provided, it will fall back to app-level config
            tags: The list of tags to set to the short URL
            title: A descriptive title of the short URL
            crawlable: Tells if this URL will be included as 'Allow' in Shlink's robots.txt
            forwardQuery:
                Tells if the query params should be forwarded from the short URL to the long one,
                as explained in the Shlink docs
        """
        data = locals()
        payload = {}
        for key, value in data.items():
            if key not in ["self", "shortCode"] and value is not MISSING:
                payload[key] = value
        data = await self._request(
            endpoint=f"/short-urls/{shortCode}", method="PATCH", data=dumps(payload)
        )
        return ShortURL.from_dict(data)

    async def get_code_visits(
        self,
        shortCode: str,
        domain: Optional[str] = MISSING,
        startDate: Optional[datetime] = MISSING,
        endDate: Optional[datetime] = MISSING,
        page: int = 1,
        itemsPerPage: Optional[int] = MISSING,
        excludeBots: bool = True,
    ) -> VisitsView:
        """
        Get the list of visits on the short URL behind provided short code.

        Args:
            shortCode: The short code for the short URL from which we want to get the visits
            domain: The domain in which the short code should be searched for
            startDate: The date from which we want to get visits
            endDate: The date until which we want to get visits
            page: The page to display, default 1
            itemsPerPage: The amount of items to return on every page
            excludeBots: Whether or not to exclude bots
        """
        data = locals()
        payload = {}
        for key, value in data.items():
            if key not in ["self", "shortCode"] and value is not MISSING:
                payload[key] = value

        data = await self._request(
            endpoint=f"/short-urls/{shortCode}/visits", method="GET", data=dumps(payload)
        )
        return VisitsView.from_dict(data)
