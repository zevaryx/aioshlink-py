from typing import Any, Dict, List, Optional, TYPE_CHECKING

from attrs import field, define

from shlink.client.utils.mixins import DictSerializationMixin

if TYPE_CHECKING:
    from shlink.client.client import Shlink


@define(slots=False)
class BaseModel(DictSerializationMixin):
    _client: Optional["Shlink"] = field()

    @classmethod
    def _process_dict(cls, data: Dict[str, Any], client: "Shlink" = None):
        return super()._process_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], client: Optional["Shlink"] = None):
        data = cls._process_dict(data, client)
        return cls(client=client, **cls._filter_kwargs(data, cls._get_init_keys()))

    @classmethod
    def from_list(cls, datas: List[Dict[str, Any]], client: "Shlink"):
        return [cls.from_dict(data, client) for data in datas]


@define(kw_only=True, slots=True)
class Pagination(DictSerializationMixin):
    currentPage: int = field()
    pagesCount: int = field()
    itemsPerPage: int = field()
    itemsInCurrentPage: int = field()
    totalItems: int = field()
