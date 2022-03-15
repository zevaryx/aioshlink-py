from datetime import datetime
from json import dumps
from typing import Optional

from shlink.models.visits import GenericVisits, VisitsView


class Visits:
    async def get_visits(self) -> GenericVisits:
        """
        Get general visits stats not linked to one specific short URL.
        """
        data = await self._request(endpoint="/visits", method="GET")
        return GenericVisits.from_dict(data)

    async def get_orphan_visits(
        self,
        startDate: Optional[datetime] = None,
        endDate: Optional[datetime] = None,
        page: int = 1,
        itemsPerPage: Optional[int] = None,
        excludeBots: bool = True,
    ) -> VisitsView:
        """
        Get the list of visits to invalid short URLs, the base URL or any other 404.

        Args:
            tag: The tag from which we want to get the visits
            startDate: The date from which we want to get visits
            endDate: The date until which we want to get visits
            page: The page to display, default 1
            itemsPerPage: The amount of items to return on every page. Defaults to all items
            excludeBots: Tells if visits from potential bots should be excluded from the result set
        """
        data = locals()
        payload = {}
        for key, value in data.items():
            if key != "self" and value:
                payload[key] = value

        data = await self._request(endpoint="/visits/orphan", method="GET", data=dumps(payload))
        return VisitsView.from_dict(data)

    async def get_nonorphan_visits(
        self,
        startDate: Optional[datetime] = None,
        endDate: Optional[datetime] = None,
        page: int = 1,
        itemsPerPage: Optional[int] = None,
        excludeBots: bool = True,
    ) -> VisitsView:
        """
        Get the list of visits to any short URL.

        Args:
            tag: The tag from which we want to get the visits
            startDate: The date from which we want to get visits
            endDate: The date until which we want to get visits
            page: The page to display, default 1
            itemsPerPage: The amount of items to return on every page. Defaults to all items
            excludeBots: Tells if visits from potential bots should be excluded from the result set
        """
        data = locals()
        payload = {}
        for key, value in data.items():
            if key != "self" and value:
                payload[key] = value

        data = await self._request(endpoint="/visits/non-orphan", method="GET", data=dumps(payload))
        return VisitsView.from_dict(data)
