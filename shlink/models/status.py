from attrs import field, define

from shlink.client.utils.mixins import DictSerializationMixin


@define(kw_only=True, slots=True)
class Links(DictSerializationMixin):
    about: str = field()
    project: str = field()


@define(kw_only=True, slots=True)
class Status(DictSerializationMixin):
    status: str = field()
    version: str = field()
    links: Links = field(converter=Links.from_dict)
