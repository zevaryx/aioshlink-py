from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from attrs import field, define

from shlink.client.const import MISSING
from shlink.client.utils.converters import list_converter, timestamp_converter
from shlink.models import BaseModel, Pagination
from shlink.models.visits import VisitsView

if TYPE_CHECKING:
    from shlink.client.client import Shlink


@define(kw_only=True, slots=True)
class Meta(BaseModel):
    validSince: Optional[datetime] = field(default=None, converter=timestamp_converter)
    validUntil: Optional[datetime] = field(default=None, converter=timestamp_converter)
    maxVisits: Optional[int] = field(default=None)


@define(kw_only=True, slots=True)
class ShortURL(BaseModel):
    shortCode: str = field()
    shortUrl: str = field()
    longUrl: str = field()
    dateCreated: datetime = field(converter=timestamp_converter)
    visitsCount: int = field()
    tags: List[str] = field(factory=list)
    meta: Meta = field(converter=Meta.from_dict)
    domain: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    crawlable: bool = field(default=False)
    forwardQuery: bool = field(default=True)

    async def delete(self) -> None:
        """Delete existing short URL."""
        await self._client.http.delete_short_url(self.shortCode)

    async def edit(
        self,
        longUrl: Optional[str],
        validSince: Optional[datetime] = MISSING,
        validUntil: Optional[datetime] = MISSING,
        maxVisits: Optional[int] = MISSING,
        validateUrl: Optional[bool] = MISSING,
        tags: Optional[List[str]] = MISSING,
        title: Optional[str] = MISSING,
        crawlable: Optional[bool] = MISSING,
        forwardQuery: Optional[bool] = MISSING,
    ) -> None:
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
        new = await self._client.http.edit_short_url(
            self.shortCode,
            longUrl,
            validSince,
            validUntil,
            maxVisits,
            validateUrl,
            tags,
            title,
            crawlable,
            forwardQuery,
        )
        self.update_from_dict(new.to_dict())

    async def visits(
        self,
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
        return await self._client.http.get_code_visits(
            self.shortCode, domain, startDate, endDate, page, itemsPerPage, excludeBots
        )


@define(kw_only=True, slots=True)
class ShortUrlsView(BaseModel):
    data: List[ShortURL] = field(
        factory=list, converter=list_converter(ShortURL.from_dict)
    )
    pagination: Pagination = field(converter=Pagination.from_dict)

    @classmethod
    def _process_dict(cls, data: Dict[str, Any], client: "Shlink"):
        data = data.pop("shortUrls")
        return super()._process_dict(data, client)

    def __attrs_post_init__(self):
        for url in self.data:
            url._client = self._client
