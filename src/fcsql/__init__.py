from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4.error.ErrorListener import ErrorListener

from .FCSLexer import FCSLexer
from .FCSParser import FCSParser
from .FCSParserListener import FCSParserListener  # noqa: F401

# ---------------------------------------------------------------------------


class SyntaxError(Exception):
    pass


class ExceptionThrowingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError(f"line {line}:{column} {msg}")


# ---------------------------------------------------------------------------


def parse(input: str) -> FCSParser.QueryContext:
    input_stream = InputStream(input)
    lexer = FCSLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = FCSParser(stream)
    parser.addErrorListener(ExceptionThrowingErrorListener())
    tree: FCSParser.QueryContext = parser.query()
    return tree


# ---------------------------------------------------------------------------
