from attrs import field, define

from shlink.models import BaseModel


@define(kw_only=True, slots=True)
class Links(BaseModel):
    about: str = field()
    project: str = field()


@define(kw_only=True, slots=True)
class Status(BaseModel):
    status: str = field()
    version: str = field()
    links: Links = field(converter=Links.from_dict)
