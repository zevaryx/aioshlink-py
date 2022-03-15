from datetime import datetime
from typing import List, Optional

from attrs import field, define

from shlink.client.utils.converters import list_converter, timestamp_converter
from shlink.client.utils.mixins import DictSerializationMixin
from shlink.models import Pagination


@define(kw_only=True, slots=True)
class Meta(DictSerializationMixin):
    validSince: Optional[datetime] = field(
        default=None, converter=timestamp_converter
    )
    validUntil: Optional[datetime] = field(
        default=None, converter=timestamp_converter
    )
    maxVisits: Optional[int] = field(default=None)


@define(kw_only=True, slots=True)
class ShortURL(DictSerializationMixin):
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


@define(kw_only=True, slots=True)
class ShortUrlsView(DictSerializationMixin):
    data: List[ShortURL] = field(factory=list, converter=list_converter(ShortURL.from_dict))
    pagination: Pagination = field(converter=Pagination.from_dict)

    @classmethod
    def _process_dict(cls, data):
        data = data.pop("shortUrls")
        return super()._process_dict(data)
