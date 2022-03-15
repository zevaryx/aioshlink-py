from typing import List, Optional

from attrs import field, define

from shlink.client.utils.converters import optional as c_optional, list_converter
from shlink.client.utils.mixins import DictSerializationMixin


@define(kw_only=True, slots=True)
class Redirect(DictSerializationMixin):
    baseUrlRedirect: Optional[str] = None
    regular404Redirect: Optional[str] = None
    invalidShortUrlRedirect: Optional[str] = None


@define(kw_only=True, slots=True)
class Domain(DictSerializationMixin):
    domain: str = field()
    isDefault: bool = field()
    redirect: Optional[Redirect] = field(default=None, converter=c_optional(Redirect.from_dict))


@define(kw_only=True, slots=True)
class DomainsView(DictSerializationMixin):
    data: List[Domain] = field(factory=list, converter=list_converter(Domain.from_dict))
    defaultRedirects: Optional[Redirect] = field(
        default=None, converter=c_optional(Redirect.from_dict))

    @classmethod
    def _process_dict(self, data):
        data = data.pop("domains")
        return super()._process_dict(data)
