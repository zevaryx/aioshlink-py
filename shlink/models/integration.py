from attrs import field, define

from shlink.models import BaseModel


@define(kw_only=True, slots=True)
class Integration(BaseModel):
    mercureHubUrl: str = field()
    jwt: str = field()
    jwtExpiration: str = field()
