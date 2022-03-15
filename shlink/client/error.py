from typing import List, Optional

from attrs import field

from shlink.client.utils.mixins import DictSerializationMixin


class _ShlinkError(DictSerializationMixin):
    type: str = field()
    title: str = field()
    detail: str = field()
    status: int = field()
    shortCode: Optional[str] = field(default=None)
    customSlug: Optional[str] = field(default=None)
    url: Optional[str] = field(default=None)
    invalidElements: Optional[List[str]] = field(default=None)


class ShlinkError(Exception):
    def __init__(self, *args, **kwargs):
        data = kwargs.pop("data", None)
        message = "Exception occurred, no further info available"
        if data:
            self.data = _ShlinkError.from_dict(
                data
            )  # DictSerializationMixin keyward 'url' error
            message = data["title"] + ": " + data["detail"]
        super().__init__(message, *args, **kwargs)
