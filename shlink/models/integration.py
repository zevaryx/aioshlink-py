from attrs import field, define

from shlink.client.utils.mixins import DictSerializationMixin


@define(kw_only=True, slots=True)
class Integration(DictSerializationMixin):
    mercureHubUrl: str = field()
    jwt: str = field()
    jwtExpiration: str = field()
