from shlink.models.status import Status


class Health:
    async def get_health(self) -> Status:
        """
        Checks the healthiness of the service, making sure it can access required resources.
        """
        data = await self._session.get(self.url + "rest/health").json()
        return Status.from_dict(data)
