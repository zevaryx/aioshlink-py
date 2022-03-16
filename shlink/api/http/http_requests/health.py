from shlink.models.status import Status


class Health:
    async def get_health(self) -> Status:
        """
        Checks the healthiness of the service, making sure it can access required resources.
        """
        resp = await self.__session.get("/rest/health")
        data = await resp.json()
        return Status.from_dict(data, self._client)
