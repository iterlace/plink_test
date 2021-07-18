import os
from typing import Any, Dict, Optional, Type, TypeVar

from system.settings.exceptions import ImproperlyConfigured

__all__ = ["get_option", "print_options"]

# Requested environment variables
_options_dict: Dict[str, Any] = {}

_None = TypeVar("_None")


def get_option(
    name: str,
    option_type: Type[Any] = str,
    default: Optional[Any] = _None,
    *,
    log: bool = True,
    secret: bool = False,
) -> Any:
    """
    Returns environment variable
    :param name: Name of the environment variable
    :param option_type: type to cast the value into
    :param default: default value, if it isn't present in environment variables
    :param log: should `name: value` be mentioned by print_options function
                in the future
    :param secret: if value contains secret value, eg passwords
    :raise ImproperlyConfigured if required variable is not set
    """
    value: Optional[Any]
    try:
        _value = os.environ[name]
        if option_type is bool:
            value = bool(int(_value))
        else:
            value = option_type(_value)
    except KeyError:
        if default is _None:
            raise ImproperlyConfigured(
                "`{}` environment variable is required!".format(name)
            )
        else:
            value = default

    if log:
        if secret:
            _options_dict[name] = "********"
        else:
            _options_dict[name] = value

    return value


def print_options() -> None:
    print("\nCurrent environment variables options:")
    for name, value in _options_dict.items():
        print(" " * 5 + "@ {} = {}".format(name, value))
    print()
