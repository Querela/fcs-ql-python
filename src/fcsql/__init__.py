from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4.error.ErrorListener import ErrorListener

from fcsql.FCSLexer import FCSLexer
from fcsql.FCSParser import FCSParser
from fcsql.FCSParserListener import FCSParserListener  # noqa: F401
from fcsql.FCSParserVisitor import FCSParserVisitor  # noqa: F401
from fcsql.parser import ErrorDetail
from fcsql.parser import QueryNode
from fcsql.parser import QueryParser
from fcsql.parser import QueryParserException  # noqa: F401
from fcsql.parser import SourceLocation  # noqa: F401

# ---------------------------------------------------------------------------


class SyntaxError(Exception):
    pass


class ExceptionThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f"line {line}:{column} {msg}")


def antlr_parse(input: str) -> FCSParser.QueryContext:
    """Run the low-level ANTLR4 tokenization and parsing. This returns the parsing
    context ANTLR4 uses instead of the simplified FCS-QL query node types.

    Args:
        input: raw query string

    Returns:
        FCSParser.QueryContext: the ANTLR4 root parsing context (query)

    Throws:
        SyntaxError: if an error occurred while parsing
    """
    input_stream = InputStream(input)
    lexer = FCSLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = FCSParser(stream)
    parser.addErrorListener(ExceptionThrowingErrorListener())
    tree: FCSParser.QueryContext = parser.query()
    return tree


# ---------------------------------------------------------------------------


def parse(input: str, *, enableSourceLocations: bool = True) -> QueryNode:
    """Simple wrapper to generate a `QueryParser` and to parse some
    input string into a `QueryNode`.

    Args:
        input: raw input query string
        enableSourceLocations: whether source locations are computed for each query node

    Returns:
        QueryNode: parsed query

    Throws:
        QueryParserException: if an error occurred
    """
    parser = QueryParser(enableSourceLocations=enableSourceLocations)
    return parser.parse(input)


def can_parse(input: str):
    """Simple wrapper to check if the input string can be successfully parsed.

    Args:
        input: raw input query string

    Returns:
        bool: ``True`` if query can be parsed, ``False`` otherwise.
    """
    try:
        parse(input)
        return True
    except QueryParserException:
        return False


# ---------------------------------------------------------------------------
