from typing import Any, Dict, List, TypeVar

import attr

from shlink.client.utils import serializer


T = TypeVar("T")


# Credit dis-snek/Lepton
@attr.s()
class DictSerializationMixin:
    @classmethod
    def _get_keys(cls) -> frozenset:
        if (keys := getattr(cls, "_keys", None)) is None:
            keys = frozenset(field.name for field in attr.fields(cls))
            setattr(cls, "_keys", keys)
        return keys

    @classmethod
    def _get_init_keys(cls) -> frozenset:
        if (init_keys := getattr(cls, "_init_keys", None)) is None:
            init_keys = frozenset(
                field.name.removeprefix("_") for field in attr.fields(cls) if field.init
            )
            setattr(cls, "_init_keys", init_keys)
        return init_keys

    @classmethod
    def _filter_kwargs(cls, kwargs_dict: dict, keys: frozenset) -> dict:
        return {k: v for k, v in kwargs_dict.items() if k in keys}

    @classmethod
    def _process_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process dictionary data received from schlink api. Does cleanup and other checks to data.

        parameters:
            data: The dictionary data received from schlink api.

        returns:
            The processed dictionary. Ready to be converted into object class.

        """
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Process and converts dictionary data received from schlink api to object class instance.

        parameters:
            data: The json data received from schlink api.

        """
        if isinstance(data, cls):
            return data

        data = cls._process_dict(data)
        return cls(**cls._filter_kwargs(data, cls._get_init_keys()))

    @classmethod
    def from_list(cls, datas: List[Dict[str, Any]]):
        """
        Process and converts list data received from schlink api to object class instances.

        parameters:
            data: The json data received from schlink api.

        """
        return [cls.from_dict(data) for data in datas]

    def update_from_dict(self: T, data: Dict[str, Any]) -> T:
        """Updates object attribute(s) with new json data received from schlink api."""
        data = self._process_dict(data)
        for key, value in self._filter_kwargs(data, self._get_keys()).items():
            # todo improve
            setattr(self, key, value)

        return self

    def _check_object(self) -> None:
        """Logic to check object properties just before export to json data for sending to schlink api."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Exports object into dictionary representation, ready to be sent to schlink api.

        returns:
            The exported dictionary.

        """
        self._check_object()
        return serializer.to_dict(self)
