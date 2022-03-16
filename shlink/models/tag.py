from typing import Any, Dict, List, TYPE_CHECKING

from attrs import field, define

from shlink.client.utils.converters import list_converter
from shlink.models import BaseModel, Pagination

if TYPE_CHECKING:
    from shlink.client.client import Shlink


@define(kw_only=True, slots=True)
class TagsView(BaseModel):
    data: List[str] = field(factory=list)
    pagination: Pagination = field(converter=Pagination.from_dict)

    @classmethod
    def _process_dict(cls, data: Dict[str, Any], client: "Shlink"):
        data = data.pop("tags")
        return super()._process_dict(data, client)

    def __attrs_post_init__(self):
        for tag in self.data:
            tag._client = self._client


@define(kw_only=True, slots=True)
class TagStats(BaseModel):
    tag: str = field()
    shortUrlsCount: str = field()
    visitsCount: int = field()


@define(kw_only=True, slots=True)
class TagStatsView(BaseModel):
    data: List[TagStats] = field(
        factory=list, converter=list_converter(TagStats.from_dict)
    )
    pagination: Pagination = field(converter=Pagination.from_dict)

    @classmethod
    def _process_dict(cls, data: Dict[str, Any], client: "Shlink"):
        data = data.pop("tags")
        return super()._process_dict(data, client)

    def __attrs_post_init__(self):
        for tag in self.data:
            tag._client = self._client
