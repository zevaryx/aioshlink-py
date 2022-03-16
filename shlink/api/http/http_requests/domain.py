from json import dumps
from typing import Optional

from shlink.client.const import MISSING
from shlink.models.domain import DomainsView, Redirect


class Domain:
    async def get_domains(self) -> DomainsView:
        """
        Returns the list of all domains that have been either used for some short URL,
        or have explicitly configured redirects.
        It also includes the domain redirects, plus the default redirects that will be used for any
        non-explicitly-configured one.
        """
        data = await self.request(endpoint="/domains", method="GET")
        return DomainsView.from_dict(data, self._client)

    async def patch_domain(
        self,
        domain: str,
        baseUrlRedirect: Optional[str] = MISSING,
        regular404Redirect: Optional[str] = MISSING,
        invalidShortUrlRedirect: Optional[str] = MISSING,
    ) -> Redirect:
        """
        Sets the URLs that you want a visitor to get redirected to for
        "not found" URLs for a specific domain

        Args:
            domain: The domain's authority for which you want to set redirects
            baseUrlRedirect: URL to redirect to when a user hits the domain's base URL
            regular404Redirect:
                URL to redirect to when a user hits a not found URL other than an invalid short URL
            invalidShortUrlRedirect: URL to redirect to when a user hits an invalid short URL
        """
        data = locals()
        payload = {}
        for key, value in data.items():
            if key not in ["self", "shortCode"] and value is not MISSING:
                payload[key] = value
        data = await self.request(
            endpoint="/domains/redirects", method="PATCH", data=dumps(payload)
        )
        return Redirect.from_dict(data, self._client)
