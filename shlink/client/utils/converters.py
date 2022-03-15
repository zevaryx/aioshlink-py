import inspect
import re
import typing
from datetime import datetime

from shlink.client.const import MISSING

iso8601 = re.compile(
    r"^([\+-]?\d{4}(?!\d{2}\b))((-?)((0[1-9]|1[0-2])(\3([12]\d|0[1-9]|3[01]))?"
    r"|W([0-4]\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\d|[12]\d{2}|3([0-5]\d|6[1-6])))"
    r"([T\s]((([01]\d|2[0-3])((:?)[0-5]\d)?|24\:?00)([\.,]\d+(?!:))?)?(\17[0-5]\d"
    r"([\.,]\d+)?)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?)?)?$"
)


def timestamp_converter(timestamp: int | str | datetime) -> typing.Optional[datetime]:
    if isinstance(timestamp, datetime):
        return timestamp
    if isinstance(timestamp, str) and iso8601.match(timestamp):
        return datetime.fromisoformat(timestamp)
    if isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp)

# Credit dis-snek/Lepton


def list_converter(converter) -> typing.Callable[[list], list]:
    def convert_action(value: list) -> list:
        return [converter(element) for element in value]

    return convert_action


# Credit dis-snek/Lepton
def optional(converter: typing.Callable) -> typing.Any:
    """
    A modified version of attrs optional decorator that supports both `None` and `MISSING`

    Type annotations will be inferred from the wrapped converter's, if it
    has any.

    args:
        converter: The convertor that is used for the non-None or MISSING
    """

    def optional_converter(val) -> typing.Any:
        if val is None or val is MISSING:
            return val
        return converter(val)

    sig = None
    try:
        sig = inspect.signature(converter)
    except (ValueError, TypeError):  # inspect failed
        pass
    if sig:
        params = list(sig.parameters.values())
        if params and params[0].annotation is not inspect.Parameter.empty:
            optional_converter.__annotations__["val"] = typing.Optional[params[0].annotation]
        if sig.return_annotation is not inspect.Signature.empty:
            optional_converter.__annotations__["return"] = typing.Optional[sig.return_annotation]

    return optional_converter
