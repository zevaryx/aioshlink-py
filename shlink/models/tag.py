from typing import List

from attrs import field, define

from shlink.client.utils.converters import list_converter
from shlink.client.utils.mixins import DictSerializationMixin
from shlink.models import Pagination


@define(kw_only=True, slots=True)
class TagsView(DictSerializationMixin):
    data: List[str] = field(factory=list)
    pagination: Pagination = field(converter=Pagination.from_dict)

    @classmethod
    def _process_dict(cls, data):
        data = data.pop("tags")
        return super()._process_dict(data)


@define(kw_only=True, slots=True)
class TagStats(DictSerializationMixin):
    tag: str = field()
    shortUrlsCount: str = field()
    visitsCount: int = field()


@define(kw_only=True, slots=True)
class TagStatsView(DictSerializationMixin):
    data: List[TagStats] = field(factory=list, converter=list_converter(TagStats.from_dict))
    pagination: Pagination = field(converter=Pagination.from_dict)

    @classmethod
    def _process_dict(cls, data):
        data = data.pop("tags")
        return super()._process_dict(data)
