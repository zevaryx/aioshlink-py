from attrs import field, define

from shlink.client.utils.mixins import DictSerializationMixin


@define(kw_only=True, slots=True)
class Pagination(DictSerializationMixin):
    currentPage: int = field()
    pagesCount: int = field()
    itemsPerPage: int = field()
    itemsInCurrentPage: int = field()
    totalItems: int = field()
