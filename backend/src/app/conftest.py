from typing import Any


def pytest_runtest_setup(item: Any) -> None:
    from django.db import DEFAULT_DB_ALIAS, connections

    connections[DEFAULT_DB_ALIAS].use_debug_cursor = True


# logging.getLogger("faker").setLevel(logging.WARN)
# logging.getLogger("factory").setLevel(logging.WARN)
