import os
from itertools import chain
from itertools import repeat
from pathlib import Path
from typing import List

import pytest

from fcsql.parser import QueryNode
from fcsql.parser import QueryParser
from fcsql.parser import QueryParserException

# ---------------------------------------------------------------------------

DN_BASE = Path(__file__).parent
DN_VALID_CASES = DN_BASE / "valid"
DN_INVALID_CASES = DN_BASE / "invalid"

# ---------------------------------------------------------------------------


def load_content(name: str | os.PathLike | Path) -> List[str]:
    fname = DN_BASE / name
    with open(fname, "r") as fp:
        content = fp.read().strip()

    if "\n" in content:
        return content.split("\n")
    else:
        return [content]


def get_files(folder: str | os.PathLike | Path = DN_BASE):
    files = sorted(
        {file for file in Path(folder).iterdir() if file.name.startswith("test") and file.name.endswith(".txt")}
    )
    return files


def get_test_queries(folder: str | os.PathLike | Path = DN_BASE):
    files = get_files(folder=folder)
    queries = map(load_content, files)
    return chain.from_iterable([zip(repeat(file.name), queries) for file, queries in zip(files, queries)])


# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name,query", get_test_queries(folder=DN_VALID_CASES))
def test_parser_by_valid_sample_query(parser: QueryParser, name: str, query: str):
    node = parser.parse(query)
    assert node is not None
    assert isinstance(node, QueryNode)


@pytest.mark.parametrize("name,query", get_test_queries(folder=DN_INVALID_CASES))
def test_parser_by_invalid_sample_query(parser: QueryParser, name: str, query: str):
    with pytest.raises(QueryParserException) as exc:  # noqa: F841
        parser.parse(query)


# ---------------------------------------------------------------------------
