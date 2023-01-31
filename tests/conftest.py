import pytest

from fcsql.parser import QueryParser

# ---------------------------------------------------------------------------


@pytest.fixture
def parser():
    """QueryParser"""

    return QueryParser()


# ---------------------------------------------------------------------------
