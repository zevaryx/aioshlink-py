from datetime import datetime
from json import dumps
from typing import List, Optional

from shlink.models.tag import TagsView, TagStatsView
from shlink.models.visits import VisitsView


class Tags:
    async def get_tags(
        self,
        page: Optional[int] = 1,
        itemsPerPage: Optional[int] = None,
        searchTerm: Optional[str] = None,
        orderBy: Optional[str] = None,
    ) -> TagsView:
        """
        Returns the list of all tags used in any short URL.

        Args:
            page: The page to display. Defaults to 1
            itemsPerPage: The amount of items to return on every page. Defaults to all items
            searchTerm: A query used to filter results by searching for it on the tag name
        """
        data = await self._request(endpoint="/tags", method="GET")
        return TagsView.from_dict(data)

    async def edit_tag(self, oldName: str, newName: str) -> None:
        """
        Renames one existing tag.

        Args:
            oldName: Current name of the tag
            newName: New name of the tag
        """
        payload = {"oldName": oldName, "newName": newName}
        return await self._request(endpoint="/tags", method="PATCH", data=dumps(payload))

    async def delete_tag(self, tags: List[str]) -> None:
        """
        Deletes provided list of tags.

        Args:
            tags: The names of the tags to delete
        """
        payload = {"tags": tags}
        return await self._request(endpoint="/tags", method="DELETE", data=dumps(payload))

    async def tag_stats(
        self,
        page: Optional[int] = 1,
        itemsPerPage: Optional[int] = None,
        searchTerm: Optional[str] = None,
        orderBy: Optional[str] = None,
    ) -> TagStatsView:
        """
        Returns the list of all tags used in any short URL,
        together with the amount of short URLs and visits for it

        Args:
            page: The page to display. Defaults to 1
            itemsPerPage: The amount of items to return on every page. Defaults to all items
            searchTerm: A query used to filter results by searching for it on the tag name
        """
        payload = {
            "page": page,
            "itemsPerPage": itemsPerPage,
            "searchTerm": searchTerm,
            "orderBy": orderBy,
        }
        data = await self._request(endpoint="/tags/stats", method="GET", params=payload)
        return TagStatsView.from_dict(data)

    async def tag_visits(
        self,
        tag: str,
        startDate: Optional[datetime] = None,
        endDate: Optional[datetime] = None,
        page: int = 1,
        itemsPerPage: Optional[int] = None,
        excludeBots: bool = True,
    ) -> VisitsView:
        """
        Get the list of visits on any short URL which is tagged with provided tag.

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
            if key not in ["self", "tag"] and value:
                payload[key] = value

        data = await self._request(endpoint=f"/tags/{tag}/visits", method="GET", params=payload)
        return VisitsView.from_dict(data)
