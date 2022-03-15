import inspect
from importlib.metadata import version as _v

try:
    __version__ = _v("shlink")
except Exception:
    __version__ = "0.0.0"


# Credit dis-snek/Lepton
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# Credit dis-snek/Lepton
class Sentinel(metaclass=Singleton):
    @staticmethod
    def _get_caller_module() -> str:
        stack = inspect.stack()

        caller = stack[2][0]
        return caller.f_globals.get("__name__")

    def __init__(self):
        self.__module__ = self._get_caller_module()
        self.name = type(self).__name__

    def __repr__(self):
        return self.name

    def __reduce__(self):
        return self.name

    def __copy__(self):
        return self

    def __deepcopy__(self, _):
        return self


# Credit dis-snek/Lepton
class Missing(Sentinel):
    def __getattr__(self, *_):
        return None

    def __bool__(self):
        return False


MISSING = Missing()
