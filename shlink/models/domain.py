from typing import Any, Dict, List, Optional, TYPE_CHECKING

from attrs import field, define

from shlink.client.const import MISSING
from shlink.client.utils.converters import optional as c_optional, list_converter
from shlink.models import BaseModel

if TYPE_CHECKING:
    from shlink.client.client import Shlink


@define(kw_only=True, slots=True)
class Redirect(BaseModel):
    baseUrlRedirect: Optional[str] = None
    regular404Redirect: Optional[str] = None
    invalidShortUrlRedirect: Optional[str] = None


@define(kw_only=True, slots=True)
class Domain(BaseModel):
    domain: str = field()
    isDefault: bool = field()
    redirect: Optional[Redirect] = field(
        default=None, converter=c_optional(Redirect.from_dict)
    )

    async def edit(
        self,
        baseUrlRedirect: Optional[str] = MISSING,
        regular404Redirect: Optional[str] = MISSING,
        invalidShortUrlRedirect: Optional[str] = MISSING,
    ) -> None:
        """
        Edit an existing domain.

        Args:
            baseUrlRedirect: URL to redirect to when a user hits the domain's base URL
            regular404Redirect:
                URL to redirect to when a user hits a not found URL other than an invalid short URL
            invalidShortUrlRedirect: URL to redirect to when a user hits an invalid short URL
        """
        self.redirect = await self._client.http.patch_domain(
            self.domain, baseUrlRedirect, regular404Redirect, invalidShortUrlRedirect
        )


@define(kw_only=True, slots=True)
class DomainsView(BaseModel):
    data: List[Domain] = field(factory=list, converter=list_converter(Domain.from_dict))
    defaultRedirects: Optional[Redirect] = field(
        default=None, converter=c_optional(Redirect.from_dict)
    )

    @classmethod
    def _process_dict(self, data: Dict[str, Any], client: "Shlink"):
        data = data.pop("domains")
        return super()._process_dict(data, client)

    def __attrs_post_init__(self):
        for domain in self.data:
            domain._client = self._client
