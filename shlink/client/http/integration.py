from shlink.models.integration import Integration


class Integration:
    async def get_mercure_info(self) -> Integration:
        """
        Returns information to consume updates published by Shlink on a mercure hub.

        https://mercure.rocks/
        """
        data = await self._request(endpoint="/mercure-info", method="GET")
        return Integration.from_dict(data)
