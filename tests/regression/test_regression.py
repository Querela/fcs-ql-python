import os
from itertools import chain
from itertools import repeat
from typing import List

import pytest

from fcsql.parser import QueryNode
from fcsql.parser import QueryParser
from fcsql.parser import QueryParserException

# ---------------------------------------------------------------------------


def load_content(name: str) -> List[str]:
    base_path = os.path.dirname(__file__)
    fname = os.path.join(base_path, name)
    with open(fname, "r") as fp:
        content = fp.read().strip()

    if "\n" in content:
        return content.split("\n")
    else:
        return [content]


def get_files():
    base_path = os.path.dirname(__file__)
    files = os.listdir(base_path)
    files = [f for f in files if f.startswith("test") and f.endswith(".txt")]
    files = sorted({f for f in files})
    return files


def get_test_queries():
    files = get_files()
    queries = map(load_content, files)
    return chain.from_iterable(
        [zip(repeat(name), queries) for name, queries in zip(files, queries)]
    )


# ---------------------------------------------------------------------------


# @pytest.mark.parametrize("name", get_files())
# def test_parser_by_sample_queries(parser: QueryParser, name: str):
#     queries = load_content(name)
#
#     for query in queries:
#         node = parser.parse(query)
#         assert node is not None
#         assert isinstance(node, QueryNode)


@pytest.mark.parametrize("name,query", get_test_queries())
def test_parser_by_sample_query(parser: QueryParser, name: str, query: str):

    if name == "test12.txt":
        with pytest.raises(
            QueryParserException, match="token recognition error at: '-'"
        ):
            parser.parse(query)

    else:

        node = parser.parse(query)
        assert node is not None
        assert isinstance(node, QueryNode)


# ---------------------------------------------------------------------------
