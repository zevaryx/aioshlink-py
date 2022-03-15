from datetime import datetime
from typing import List, Optional

from attrs import field, define

from shlink.client.utils.converters import list_converter, optional as c_optional, timestamp_converter
from shlink.client.utils.mixins import DictSerializationMixin
from shlink.models import Pagination


class VisitsMixin(DictSerializationMixin):
    @classmethod
    def _process_dict(self, data):
        data = data.pop("visits")
        return super()._process_dict(data)


@define(kw_only=True, slots=True)
class GenericVisits(VisitsMixin):
    visitsCount: int = field()
    orphanVisitsCount: int = field()


@define(kw_only=True, slots=True)
class VisitLocation(DictSerializationMixin):
    cityName: str
    countryCode: str
    countryName: str
    latitude: int
    longitude: int
    regionName: str
    timezone: str


@define(kw_only=True, slots=True)
class Visit(DictSerializationMixin):
    referer: str = field()
    date: datetime = field(converter=timestamp_converter)
    userAgent: str = field()
    visitLocation: Optional[VisitLocation] = field(
        default=None, converter=c_optional(VisitLocation.from_dict))
    potentialBot: bool = field(default=False)
    visitedUrl: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)  # Only for orphan visits


@define(kw_only=True, slots=True)
class VisitsView(VisitsMixin):
    data: List[Visit] = field(factory=list, converter=list_converter(Visit.from_dict))
    pagination: Pagination = field(converter=Pagination.from_dict)
