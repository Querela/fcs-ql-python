import logging
import unicodedata
from abc import ABCMeta
from abc import abstractmethod
from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Deque
from typing import Generic
from typing import List
from typing import Literal
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeAlias
from typing import TypeVar
from typing import Union

import antlr4
import antlr4.error.ErrorListener
from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4 import ParserRuleContext
from antlr4 import Token
from antlr4.Recognizer import Recognizer
from antlr4.tree.Tree import TerminalNodeImpl

from fcsql.FCSLexer import FCSLexer
from fcsql.FCSParser import FCSParser
from fcsql.FCSParserVisitor import FCSParserVisitor

# ---------------------------------------------------------------------------

LOGGER = logging.getLogger(__name__)


_T = TypeVar("_T", bound="QueryNode")
"""Type of ``QueryNode``."""
_R = TypeVar("_R")
"""Result type for ``QueryVisitor``."""
_UnicodeNormalizationForm: TypeAlias = Literal["NFC", "NFD", "NFKC", "NFKD"]


OCCURS_UNBOUNDED = -1
"""Atom occurrence if not bound."""

# ---------------------------------------------------------------------------


class QueryNodeType(str, Enum):
    """Node types of FCS-QL expression tree nodes."""

    def __str__(self) -> str:
        return self.value

    QUERY_SEGMENT = "QuerySegment"
    """Segment query."""
    QUERY_GROUP = "QueryGroup"
    """Group query."""
    QUERY_SEQUENCE = "QuerySequence"
    """Sequence query."""
    QUERY_DISJUNCTION = "QueryDisjunction"
    """Or query."""
    QUERY_WITH_WITHIN = "QueryWithWithin"
    """Query with within part."""

    EXPRESSION = "Expression"
    """Simple expression."""
    EXPRESSION_WILDCARD = "Wildcard"
    """Wildcard expression."""
    EXPRESSION_GROUP = "Group"
    """Group expression."""
    EXPRESSION_OR = "Or"
    """Or expression."""
    EXPRESSION_AND = "And"
    """And expression."""
    EXPRESSION_NOT = "Not"
    """Not expression."""

    SIMPLE_WITHIN = "SimpleWithin"
    """Simple within part."""


class Operator(str, Enum):
    """FCS-QL operators."""

    def __str__(self) -> str:
        return self.value

    EQUALS = "Eq"
    """EQUALS operator."""
    NOT_EQUALS = "Ne"
    """NOT-EQUALS operator."""


class RegexFlag(str, Enum):
    """FCS-QL expression tree regex flags."""

    def __new__(cls, name: str, char: str):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj.char = char
        return obj

    char: str

    def __str__(self) -> str:
        return self.value

    CASE_INSENSITIVE = ("case-insensitive", "i")
    """Case insensitive."""
    CASE_SENSITIVE = ("case-sensitive", "I")
    """Case sensitive."""
    LITERAL_MATCHING = ("literal-matching", "l")
    """match exactly (= literally)"""
    IGNORE_DIACRITICS = ("ignore-diacritics", "d")
    """Ignore all diacritics."""


class SimpleWithinScope(str, Enum):
    """The within scope."""

    def __str__(self) -> str:
        return self.value

    SENTENCE = "Sentence"
    """sentence scope (small)"""
    UTTERANCE = "Utterance"
    """utterance scope (small)"""
    PARAGRAPH = "Paragraph"
    """paragraph scope (medium)"""
    TURN = "Turn"
    """turn scope (medium)"""
    TEXT = "Text"
    """text scope (large)"""
    SESSION = "Session"
    """session scope (large)"""


# ---------------------------------------------------------------------------


class QueryVisitor(Generic[_R], metaclass=ABCMeta):
    """Interface implementing a Visitor pattern for FCS-QL expression trees.

    Default method implementations do nothing.
    """

    def visit(self, node: "QueryNode") -> Optional[_R]:
        """Visit a query node. Generic handler, dispatches to visit methods
        based on `QueryNodeType` if exists else do nothing::

            method = "visit_" + node.node_type.value

        Args:
            node: the node to visit

        Returns:
            _R: visitation result or ``None`` (see `defaultResult()`)
        """
        if not node:
            return None

        def noop(node):
            return self.defaultResult()

        # search for specific visit function based on node_type
        method_name = f"visit_{node.node_type}"
        method = getattr(self, method_name, noop)

        return method(node)

    # ----------------------------------------------------
    # same as antlr4.tree.Tree.ParseTreeVisitor

    def visitChildren(self, node: "QueryNode") -> Optional[_R]:
        result = self.defaultResult()
        for i in range(node.child_count):
            if not self.shouldVisitNextChild(node, result):
                return result

            child = node.get_child(i)
            assert child is not None, f"child#{i} must not be None in {node=}"
            childResult = child.accept(self)
            result = self.aggregateResult(result, childResult)

        return result

    def defaultResult(self) -> Optional[_R]:
        return None

    def aggregateResult(self, aggregate: Optional[_R], nextResult: Optional[_R]) -> Optional[_R]:
        return nextResult

    def shouldVisitNextChild(self, node: "QueryNode", currentResult: Optional[_R]) -> bool:
        return True


class QueryVisitorAdapter(QueryVisitor[_R]):
    """This class provides an empty implementation of ``QueryVisitor``,
    which can be extended to create a visitor which only needs to handle
    a subset of the available methods.

    Generic with regards to the return type of the visit operation.
    """

    def visit_Expression(self, node: "Expression") -> Optional[_R]:
        """Visit a SIMPLE expression query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_ExpressionWildcard(self, node: "ExpressionWildcard") -> Optional[_R]:
        """Visit a WILDCARD expression query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_ExpressionGroup(self, node: "ExpressionGroup") -> Optional[_R]:
        """Visit a GROUP expression query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_ExpressionNot(self, node: "ExpressionNot") -> Optional[_R]:
        """Visit a NOT expression query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_ExpressionAnd(self, node: "ExpressionAnd") -> Optional[_R]:
        """Visit a AND expression query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_ExpressionOr(self, node: "ExpressionOr") -> Optional[_R]:
        """Visit a OR expression query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_QueryDisjunction(self, node: "QueryDisjunction") -> Optional[_R]:
        """Visit a QR query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_QuerySequence(self, node: "QuerySequence") -> Optional[_R]:
        """Visit a query sequence node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_QueryWithWithin(self, node: "QueryWithWithin") -> Optional[_R]:
        """Visit a QUERY-WITH-WITHIN query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_QuerySegment(self, node: "QuerySegment") -> Optional[_R]:
        """Visit a query segment node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_QueryGroup(self, node: "QueryGroup") -> Optional[_R]:
        """Visit a GROUP query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)

    def visit_SimpleWithin(self, node: "SimpleWithin") -> Optional[_R]:
        """Visit a GROUP query node.

        Args:
            node: the node to visit

        Returns:
            _R: visitation result
        """
        return self.visitChildren(node)


# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceLocation:
    """Source information wrapping start and stop offsets in the query text for a query node."""

    start: int
    """Start offset in raw query string"""
    stop: int
    """End offset in raw query string"""

    @staticmethod
    def fromContext(ctx: ParserRuleContext):
        if not ctx:
            return None

        # start and stop tokens might be null (maybe due to errors)
        if ctx.start is None or ctx.stop is None:
            return None

        start = ctx.start.start
        stop = ctx.stop.stop + 1
        # NOTE: stop+1 for Java/Python string indexing
        return SourceLocation(start, stop)

    @staticmethod
    def fromToken(tok: Token):
        if tok.start is None or tok.start == -1:
            return None
        if tok.stop is None or tok.stop == -1:
            return None

        start = tok.start
        stop = tok.stop + 1
        # NOTE: stop+1 for Java/Python string indexing
        return SourceLocation(start, stop)

    def __str__(self):
        return f"{self.start}:{self.stop}"


class QueryNode(Generic[_R], metaclass=ABCMeta):
    """Base class for FCS-QL expression tree nodes."""

    def __init__(
        self,
        node_type: QueryNodeType,
        *,
        children: Optional[List["QueryNode"]] = None,
        child: Optional["QueryNode"] = None,
        location: Optional[SourceLocation] = None,
    ):
        """[Constructor]

        Args:
            node_type: the type of the node
            children: the children of this node or ``None``. Defaults to None.
            child: the child of this node or ``None``. Defaults to None.
            location: the source code location for this query node
                      in the query text content or ``None``. Defaults to None.
        """
        self.node_type = node_type
        """The node type of this node."""

        self.parent: Optional[QueryNode] = None
        """The parent node of this node.

        ``None`` if this is the root node.
        """

        if not children:
            children = list()

        self.children = list(children)
        """The children of this node."""

        if child:
            self.children.append(child)

        # update parents in children
        for child in self.children:
            child.parent = self

        self.location: Optional[SourceLocation] = location
        """source location information about start/stop offsets for this query node in the query text content"""

    def has_node_type(self, node_type: QueryNodeType) -> bool:
        """Check, if node if of given type.

        Args:
            node_type: type to check against

        Returns:
            bool: ``True`` if node is of given type, ``False`` otherwise

        Raises:
            TypeError: if node_type is ``None``
        """
        if node_type is None:
            raise TypeError("node_type is None")
        return self.node_type == node_type

    @property
    def child_count(self) -> int:
        """Get the number of children of this node.

        Returns:
            int: the number of children of this node
        """
        return len(self.children) if self.children else 0

    def get_child(self, idx: int, clazz: Optional[Type[_T]] = None) -> Optional["QueryNode"]:
        """Get a child node of specified type by index.

        When supplied with ``clazz`` parameter, only child nodes of
        the requested type are counted.

        Args:
            idx: the index of the child node (if `clazz` provided, only consideres child nodes
                 of requested type)
            clazz: the type to nodes to be considered, optional

        Returns:
            QueryNode: the child node of this node or ``None`` if not child was found
                       (e.g. type mismatch or index out of bounds)
        """
        if not self.children or idx < 0 or idx > self.child_count:
            return None
        if not clazz:
            return self.children[idx]
        pos = 0
        for child in self.children:
            if isinstance(child, clazz):
                if pos == idx:
                    return child
                pos += 1
        return None

    def get_first_child(self, clazz: Optional[Type[_T]] = None) -> Optional["QueryNode"]:
        """Get this first child node.

        Args:
            clazz: the type to nodes to be considered

        Returns:
            QueryNode: the first child node of this node or ``None``
        """
        return self.get_child(0, clazz=clazz)

    def get_last_child(self, clazz: Optional[Type[_T]] = None) -> Optional["QueryNode"]:
        """Get this last child node.

        Args:
            clazz: the type to nodes to be considered

        Returns:
            QueryNode: the last child node of this node or ``None``
        """
        return self.get_child(self.child_count - 1, clazz=clazz)

    def __str__(self) -> str:
        chs = " ".join(map(str, self.children))
        strrepr = f"({self.node_type!s}{' ' + chs if chs else ''})"
        if self.location:
            strrepr += f"@{self.location.start}:{self.location.stop}"
        return strrepr

    @abstractmethod
    def accept(self, visitor: QueryVisitor) -> _R:
        pass


# ---------------------------------------------------------------------------


class Expression(QueryNode):
    """A FCS-QL expression tree SIMPLE expression node."""

    def __init__(
        self,
        qualifier: Optional[str],
        identifier: str,
        operator: Operator,
        regex: str,
        regex_flags: Optional[Set[RegexFlag]],
    ):
        """[Constructor]

        Args:
            qualifier: the layer identifier qualifier or ``None``
            identifier: the layer identifier
            operator: the operator
            regex: the regular expression
            regex_flags: the regular expression flags or ``None``
        """

        super().__init__(QueryNodeType.EXPRESSION)

        if not qualifier or qualifier.isspace():
            qualifier = None
        if not regex_flags:
            regex_flags = None
        else:
            regex_flags = set(regex_flags)

        self.qualifier = qualifier
        """The Layer Type Identifier qualifier.

        ``None`` if not used in this expression.
        """
        self.identifier = identifier
        """The layer identifier."""
        self.operator = operator
        """The operator."""
        self.regex = regex
        """The regex value."""
        self.regex_flags = regex_flags
        """The regex flags set.

        ``None`` if no flags were used in this expression.
        """

    def has_layer_identifier(self, identifier: str) -> bool:
        """Check if the expression used a given **Layer Type Identifier**.

        Args:
            identifier: the Layer Type Identifier to check against

        Returns:
            bool: ``True`` if this identifier was used, ``False`` otherwise

        Raises:
            TypeError: if identifier is ``None``
        """
        if identifier is None:
            raise TypeError("identifier is None")
        return self.identifier == identifier

    def is_layer_qualifier_empty(self) -> bool:
        """Check if the Layer Type Identifier qualifier is empty.

        Returns:
            bool: ``True`` if no Layer Type Identifier qualifier was set, ``False`` otherwise
        """
        # NOTE: check only `self.qualifier is None` ?
        return bool(self.qualifier)

    def has_layer_qualifier(self, qualifier: str) -> bool:
        """Check if the expression used a given qualifier for the Layer Type
        Identifier.

        Args:
            qualifier: the qualifier to check against

        Returns:
            bool: ``True`` if this identifier was used, ``False`` otherwise

        Raises:
            TypeError: if qualifier is ``None``
        """
        if qualifier is None:
            raise TypeError("qualifier is None")
        if self.is_layer_qualifier_empty():
            return False
        return self.qualifier == qualifier

    def has_operator(self, operator: Operator) -> bool:
        """Check if expression used a given operator.

        Args:
            operator: the operator to check

        Returns:
            bool: ``True`` if the given operator was used, ``False`` otherwise

        Raises:
            TypeError: if operator is ``None``
        """
        if operator is None:
            raise TypeError("operator is None")
        return self.operator == operator

    def is_regex_flags_empty(self) -> bool:
        """Check if a regex flag set is empty.

        Returns:
            bool: ``True`` if no regex flags where set, ``False`` otherwise
        """
        return bool(self.regex_flags)

    def has_regex_flag(self, flag: RegexFlag) -> bool:
        """Check if a regex flag is set.

        Args:
            flag: the flag to be checked

        Returns:
            bool: ``True`` if the flag is set, ``False`` otherwise

        Raises:
            TypeError: if flag is ``None``
        """
        if flag is None:
            raise TypeError("flag is None")
        if not self.regex_flags:
            return False
        return flag in self.regex_flags

    def __str__(self) -> str:
        parts = list()
        parts.append(f"({self.node_type!s} ")
        parts.append(f"{self.qualifier}:" if self.qualifier else "")
        parts.append(f'{self.identifier} {self.operator!s} "')
        parts.append(self.regex.translate(str.maketrans({"\n": "\\n", "\r": "\\r", "\t": "\\t"})))  # type: ignore
        parts.append('"')
        if self.regex_flags:
            parts.append("/")
            # TODO: use chars from RegexFlag enum. How to guarantee same order?
            parts.append("i" if RegexFlag.CASE_INSENSITIVE in self.regex_flags else "")
            parts.append("I" if RegexFlag.CASE_SENSITIVE in self.regex_flags else "")
            parts.append("l" if RegexFlag.LITERAL_MATCHING in self.regex_flags else "")
            parts.append("d" if RegexFlag.IGNORE_DIACRITICS in self.regex_flags else "")
        parts.append(")")
        if self.location:
            parts.append(f"@{self.location.start}:{self.location.stop}")
        return "".join(parts)

    def accept(self, visitor: QueryVisitor) -> None:
        visitor.visit(self)


# ---------------------------------------------------------------------------


class ExpressionWildcard(QueryNode):
    """A FCS-QL expression tree WILDCARD expression node."""

    def __init__(
        self,
        children: Optional[List["QueryNode"]] = None,
        child: Optional["QueryNode"] = None,
    ):
        super().__init__(QueryNodeType.EXPRESSION_WILDCARD, children=children, child=child)

    def accept(self, visitor: QueryVisitor) -> None:
        visitor.visit(self)


class ExpressionGroup(QueryNode):
    """A FCS-QL expression tree GROUP expression node."""

    def __init__(self, child: QueryNode):
        """[Constructor]

        Args:
            child: the group content
        """
        super().__init__(QueryNodeType.EXPRESSION_GROUP, child=child)

    def __str__(self) -> str:
        strrepr = f"({self.node_type!s} {self.get_first_child()!s})"
        if self.location:
            strrepr += f"@{self.location.start}:{self.location.stop}"
        return strrepr

    def accept(self, visitor: QueryVisitor) -> None:
        if self.children:
            # for child in self.children:
            #     child.accept(visitor)
            self.children[0].accept(visitor)
        visitor.visit(self)


class ExpressionNot(QueryNode):
    """A FCS-QL expression tree NOT expression node."""

    def __init__(self, child: QueryNode):
        """[Constructor]

        Args:
            child: the child expression
        """
        super().__init__(QueryNodeType.EXPRESSION_NOT, child=child)

    def __str__(self) -> str:
        return f"({self.node_type!s} {self.get_first_child()!s})"

    def accept(self, visitor: QueryVisitor) -> None:
        if self.children:
            # for child in self.children:
            #     child.accept(visitor)
            self.children[0].accept(visitor)
        visitor.visit(self)


class ExpressionAnd(QueryNode):
    """A FCS-QL expression tree AND expression node."""

    def __init__(self, children: List[QueryNode]):
        """[Constructor]

        Args:
            children: child elements covered by AND expression.
        """
        super().__init__(QueryNodeType.EXPRESSION_AND, children=children)

    @property
    def operands(self) -> List[QueryNode]:
        """Get the AND expression operands.

        Returns:
            List[QueryNode]: a list of expressions
        """
        return self.children

    def accept(self, visitor: QueryVisitor) -> None:
        if self.children:
            for child in self.children:
                child.accept(visitor)
        visitor.visit(self)


class ExpressionOr(QueryNode):
    """A FCS-QL expression tree OR expression node."""

    def __init__(self, children: List[QueryNode]):
        """[Constructor]

        Args:
            children: child elements covered by OR expression.
        """
        super().__init__(QueryNodeType.EXPRESSION_OR, children=children)

    @property
    def operands(self) -> List[QueryNode]:
        """Get the OR expression operands.

        Returns:
            List[QueryNode]: a list of expressions
        """
        return self.children

    def accept(self, visitor: QueryVisitor) -> None:
        if self.children:
            for child in self.children:
                child.accept(visitor)
        visitor.visit(self)


# ---------------------------------------------------------------------------


class QueryDisjunction(QueryNode):
    """A FCS-QL expression tree QR query."""

    def __init__(self, children: List[QueryNode]):
        """[Constructor]

        Args:
            children: the children
        """
        super().__init__(QueryNodeType.QUERY_DISJUNCTION, children=children)

    def accept(self, visitor: QueryVisitor) -> None:
        if self.children:
            for child in self.children:
                child.accept(visitor)
        visitor.visit(self)


class QuerySequence(QueryNode):
    """A FCS-QL expression tree query sequence node."""

    def __init__(self, children: List[QueryNode]):
        """[Constructor]

        Args:
            children: the children for this node
        """
        super().__init__(QueryNodeType.QUERY_SEQUENCE, children=children)

    def accept(self, visitor: QueryVisitor) -> None:
        if self.children:
            for child in self.children:
                child.accept(visitor)
        visitor.visit(self)


class QueryWithWithin(QueryNode):
    """FCS-QL expression tree QUERY-WITH-WITHIN node."""

    def __init__(self, query: QueryNode, within: Optional[QueryNode]):
        """[Constructor]

        Args:
            query: the query node
            within: the within node
        """
        children = [query, within] if within else [query]
        super().__init__(QueryNodeType.QUERY_WITH_WITHIN, children=children)

    def get_query(self) -> QueryNode:
        """Get the query clause.

        Returns:
            QueryNode: the query clause
        """
        return self.children[0]

    def get_within(self) -> Optional[QueryNode]:
        """Get the within clause (= search context)

        Returns:
            QueryNode: the witin clause
        """
        return self.get_child(1)

    def accept(self, visitor: QueryVisitor) -> None:
        self.children[0].accept(visitor)
        within = self.get_child(1)
        if within:
            within.accept(visitor)
        visitor.visit(self)


class QuerySegment(QueryNode):
    """A FCS-QL expression tree query segment node."""

    def __init__(self, expression: QueryNode, min_occurs: int, max_occurs: int):
        """[Constructor]

        Args:
            expression: the expression
            min_occurs: the minimum occurrence
            max_occurs: the maximum occurrence
        """
        super().__init__(QueryNodeType.QUERY_SEGMENT, child=expression)

        self.min_occurs = min_occurs
        """The minimum occurrence of this segment."""
        self.max_occurs = max_occurs
        """The maximum occurrence of this segment."""

    def get_expression(self) -> QueryNode:
        """Get the expression for this segment.

        Returns:
            QueryNode: the expression
        """
        return self.children[0]

    def __str__(self) -> str:
        strrepr = f"({self.node_type!s} "
        if self.min_occurs != 1:
            strrepr += f"@min={'*' if self.min_occurs == OCCURS_UNBOUNDED else self.min_occurs} "
        if self.max_occurs != 1:
            strrepr += f"@max={'*' if self.max_occurs == OCCURS_UNBOUNDED else self.max_occurs} "
        strrepr += f"{self.children[0]!s})"
        if self.location:
            strrepr += f"@{self.location.start}:{self.location.stop}"
        return strrepr

    def accept(self, visitor: QueryVisitor) -> None:
        self.children[0].accept(visitor)
        visitor.visit(self)


class QueryGroup(QueryNode):
    """A FCS-QL expression tree GROUP query node."""

    def __init__(self, child: QueryNode, min_occurs: int, max_occurs: int):
        """[Constructor]

        Args:
            child: the child
            min_occurs: the minimum occurrence
            max_occurs: the maximum occurrence
        """
        super().__init__(QueryNodeType.QUERY_SEGMENT, child=child)

        self.min_occurs = min_occurs
        """The minimum occurrence of group content."""
        self.max_occurs = max_occurs
        """The maximum occurrence of group content."""

    def get_content(self) -> QueryNode:
        """Get the group content.

        Returns:
            QueryNode: the content of the GROUP query
        """
        return self.children[0]

    def __str__(self) -> str:
        strrepr = f"({self.node_type!s} "
        if self.min_occurs != 1:
            strrepr += f"@min={'*' if self.min_occurs == OCCURS_UNBOUNDED else self.min_occurs} "
        if self.max_occurs != 1:
            strrepr += f"@max={'*' if self.max_occurs == OCCURS_UNBOUNDED else self.max_occurs} "
        strrepr += f"{self.children[0]!s})"
        if self.location:
            strrepr += f"@{self.location.start}:{self.location.stop}"
        return strrepr

    def accept(self, visitor: QueryVisitor) -> None:
        if self.children:
            for child in self.children:
                child.accept(visitor)
        visitor.visit(self)


# ---------------------------------------------------------------------------


class SimpleWithin(QueryNode):
    """A FCS-QL expression tree SIMPLE WITHIN query node."""

    def __init__(self, scope: SimpleWithinScope):
        super().__init__(QueryNodeType.SIMPLE_WITHIN)

        self.scope = scope
        """The simple within scope."""

    def __str__(self) -> str:
        strrepr = f"({self.node_type!s} {self.scope!s})"
        if self.location:
            strrepr += f"@{self.location.start}:{self.location.stop}"
        return strrepr

    def accept(self, visitor: QueryVisitor) -> None:
        visitor.visit(self)


# ---------------------------------------------------------------------------


REP_ZERO_OR_MORE = (0, OCCURS_UNBOUNDED)
REP_ONE_OR_MORE = (1, OCCURS_UNBOUNDED)
REP_ZERO_OR_ONE = (0, 1)

EMPTY_STRING = ""

DEFAULT_IDENTIFIER = "text"
DEFAULT_OPERATOR = Operator.EQUALS
DEFAULT_UNICODE_NORMALIZATION_FORM: _UnicodeNormalizationForm = "NFC"
"""Default unicode normalization form.

See also: `unicodedata.normalize
<https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize>`_
"""


# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ErrorDetail:
    """Wrapper for error or warnings messages to include the type of issue
    with optional position and query string fragment."""

    message: str
    """the error or warning message"""
    type: Optional[Union[Literal["syntax-error", "validation-error", "validation-warning"], str]] = None
    """the type of error or warning"""
    position: Optional[Union[int, SourceLocation]] = None
    """optional position information in the raw query string"""
    fragment: Optional[str] = None
    """optional query string fragment, may be a substring to quickly locate the issue"""


class ErrorListener(antlr4.error.ErrorListener.ErrorListener):
    def __init__(self, query: str) -> None:
        super().__init__()
        self.query = query
        self.errors: List[ErrorDetail] = list()

    def syntaxError(
        self, recognizer: Recognizer, offendingSymbol: Optional[Token], line: int, column: int, msg: str, e
    ):
        # FIXME: additional information of error should not be logged but added
        # to the list of errors; that list probably needs to be enhanced to
        # store supplementary information Furthermore, a sophisticated
        # errorlist implementation could also be used by the QueryVistor to add
        # addition query error information

        pos = None
        fragment = None
        if isinstance(offendingSymbol, Token):
            pos = offendingSymbol.start
            fragment = self.query[: pos + len(offendingSymbol.text)]

        if LOGGER.isEnabledFor(logging.DEBUG):
            if pos is not None and pos != -1:
                LOGGER.debug("query: %s", self.query)
                LOGGER.debug("       %s^- %s", " " * pos, msg)

            if isinstance(recognizer, FCSParser) and isinstance(offendingSymbol, Token):
                LOGGER.debug("symbol: %s", recognizer.symbolicNames[offendingSymbol.type])
                LOGGER.debug("literal: %s", recognizer.literalNames[offendingSymbol.type])
                LOGGER.debug("token idx: %s", offendingSymbol.tokenIndex)

        if pos is None:
            pos = column

        self.errors.append(
            ErrorDetail(
                message=msg,
                type="syntax-error",
                position=SourceLocation.fromToken(offendingSymbol) if isinstance(offendingSymbol, Token) else pos,
                fragment=fragment,
            )
        )

    def has_errors(self) -> bool:
        return bool(self.errors)


class QueryParserException(Exception):
    """Query parser exception."""


class ExpressionTreeBuilderException(Exception):
    """Error building expression tree."""


class ExpressionTreeBuilder(FCSParserVisitor):
    def __init__(self, parser: "QueryParser") -> None:
        super().__init__()
        self.parser = parser
        self.stack: Deque[Any] = deque()

    # ----------------------------------------------------

    def visitQuery(self, ctx: FCSParser.QueryContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitQuery/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        super().visitQuery(ctx)

        w_ctx = ctx.within_part()
        if w_ctx is not None:
            within = self.stack.pop()
            query = self.stack.pop()
            node = QueryWithWithin(query, within)
            if self.parser.enableSourceLocations:
                node.location = SourceLocation.fromContext(ctx)
            self.stack.append(node)

        LOGGER.debug("visitQuery/exit: stack=%s", self.stack)
        return None

    def visitMain_query(self, ctx: FCSParser.Main_queryContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitMain_query/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        super().visitMain_query(ctx)

        LOGGER.debug("visitMain_query/exit: stack=%s", self.stack)
        return None

    def visitQuery_disjunction(self, ctx: FCSParser.Query_disjunctionContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitQuery_disjunction/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        pos = len(self.stack)

        super().visitQuery_disjunction(ctx)

        if len(self.stack) > pos:
            items: List[QueryNode] = list()
            while len(self.stack) > pos:
                items.insert(0, self.stack.pop())

            node = QueryDisjunction(items)
            if self.parser.enableSourceLocations:
                node.location = SourceLocation.fromContext(ctx)
            self.stack.append(node)
        else:
            raise ExpressionTreeBuilderException("visitQuery_disjunction is empty")

        LOGGER.debug("visitQuery_disjunction/exit: stack=%s", self.stack)
        return None

    def visitQuery_sequence(self, ctx: FCSParser.Query_sequenceContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitQuery_sequence/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        pos = len(self.stack)

        super().visitQuery_sequence(ctx)

        if len(self.stack) > pos:
            items: List[QueryNode] = list()
            while len(self.stack) > pos:
                items.insert(0, self.stack.pop())

            node = QuerySequence(items)
            if self.parser.enableSourceLocations:
                node.location = SourceLocation.fromContext(ctx)
            self.stack.append(node)
        else:
            raise ExpressionTreeBuilderException("visitQuery_sequence is empty")

        LOGGER.debug("visitQuery_sequence/exit: stack=%s", self.stack)
        return None

    def visitQuery_group(self, ctx: FCSParser.Query_groupContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitQuery_group/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        super().visitQuery_group(ctx)

        # handle repetition (if any)
        min = max = 1

        # fetch *first* child of type QuantifierContext, therefore idx=0
        q_ctx = ctx.quantifier()
        if q_ctx is not None:
            min, max = ExpressionTreeBuilder.processRepetition(q_ctx)

        content: QueryNode = self.stack.pop()
        node = QueryGroup(content, min, max)
        if self.parser.enableSourceLocations:
            node.location = SourceLocation.fromContext(ctx)
        self.stack.append(node)

        LOGGER.debug("visitQuery_group/exit: stack=%s", self.stack)
        return None

    def visitQuery_simple(self, ctx: FCSParser.Query_simpleContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitQuery_simple/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        super().visitQuery_simple(ctx)

        # handle repetition (if any)
        min = max = 1

        # fetch *first* child of type QuantifierContext, therefore idx=0
        q_ctx = ctx.quantifier()
        if q_ctx is not None:
            min, max = ExpressionTreeBuilder.processRepetition(q_ctx)

        expression: QueryNode = self.stack.pop()
        node = QuerySegment(expression, min, max)
        if self.parser.enableSourceLocations:
            node.location = SourceLocation.fromContext(ctx)
        self.stack.append(node)

        LOGGER.debug("visitQuery_simple/exit: stack=%s", self.stack)
        return None

    def visitQuery_implicit(self, ctx: FCSParser.Query_implicitContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitQuery_implicit/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        self.stack.append(self.parser.default_operator)
        self.stack.append(self.parser.default_identifier)
        self.stack.append(EMPTY_STRING)

        super().visitQuery_implicit(ctx)

        regex_flags: Set[RegexFlag] = self.stack.pop()
        regex_value: str = self.stack.pop()
        qualifier: str = self.stack.pop()
        identifier: str = self.stack.pop()
        operator: Operator = self.stack.pop()

        node = Expression(
            qualifier=qualifier,
            identifier=identifier,
            operator=operator,
            regex=regex_value,
            regex_flags=regex_flags,
        )
        if self.parser.enableSourceLocations:
            node.location = SourceLocation.fromContext(ctx)
        self.stack.append(node)

        LOGGER.debug("visitQuery_implicit/exit: stack=%s", self.stack)
        return None

    def visitQuery_segment(self, ctx: FCSParser.Query_segmentContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitQuery_segment/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        # if the context contains only two children, they must be
        # '[' and ']' thus we are dealing with a wildcard segment
        if ctx.getChildCount() == 2:
            node = ExpressionWildcard()
            if self.parser.enableSourceLocations:
                node.location = SourceLocation.fromContext(ctx)
            self.stack.append(node)

        else:
            super().visitQuery_segment(ctx)

        LOGGER.debug("visitQuery_segment/exit: stack=%s", self.stack)
        return None

    def visitExpression_basic(self, ctx: FCSParser.Expression_basicContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitExpression_basic/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        if ctx.OPERATOR_EQ() is not None:
            self.stack.append(Operator.EQUALS)
        elif ctx.OPERATOR_NE() is not None:
            self.stack.append(Operator.NOT_EQUALS)
        else:
            tok_ok = ctx.getChild(0)
            tok_ok_text = tok_ok.text if tok_ok else tok_ok
            raise ExpressionTreeBuilderException(f"invalid operator type: {tok_ok_text}")

        super().visitExpression_basic(ctx)

        regex_flags: Set[RegexFlag] = self.stack.pop()
        regex_value: str = self.stack.pop()
        qualifier: str = self.stack.pop()
        identifier: str = self.stack.pop()
        operator: Operator = self.stack.pop()

        node = Expression(
            qualifier=qualifier,
            identifier=identifier,
            operator=operator,
            regex=regex_value,
            regex_flags=regex_flags,
        )
        if self.parser.enableSourceLocations:
            node.location = SourceLocation.fromContext(ctx)
        self.stack.append(node)

        LOGGER.debug("visitExpression_basic/exit: stack=%s", self.stack)
        return None

    def visitExpression_not(self, ctx: FCSParser.Expression_notContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitExpression_not/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        super().visitExpression_not(ctx)

        expression: QueryNode = self.stack.pop()
        node = ExpressionNot(expression)
        if self.parser.enableSourceLocations:
            node.location = SourceLocation.fromContext(ctx)
        self.stack.append(node)

        LOGGER.debug("visitExpression_not/exit: stack=%s", self.stack)
        return None

    def visitExpression_group(self, ctx: FCSParser.Expression_groupContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitExpression_group/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        super().visitExpression_group(ctx)

        expression: QueryNode = self.stack.pop()
        node = ExpressionGroup(expression)
        if self.parser.enableSourceLocations:
            node.location = SourceLocation.fromContext(ctx)
        self.stack.append(node)

        LOGGER.debug("visitExpression_group/exit: stack=%s", self.stack)
        return None

    def visitExpression_or(self, ctx: FCSParser.Expression_orContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitExpression_or/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        pos = len(self.stack)

        super().visitExpression_or(ctx)

        if len(self.stack) > pos:
            children: List[QueryNode] = list()
            while len(self.stack) > pos:
                children.insert(0, self.stack.pop())

            node = ExpressionOr(children)
            if self.parser.enableSourceLocations:
                node.location = SourceLocation.fromContext(ctx)
            self.stack.append(node)
        else:
            raise ExpressionTreeBuilderException("visitExpression_or is empty")

        LOGGER.debug("visitExpression_or/exit: stack=%s", self.stack)
        return None

    def visitExpression_and(self, ctx: FCSParser.Expression_andContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitExpression_and/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        pos = len(self.stack)

        super().visitExpression_and(ctx)

        if len(self.stack) > pos:
            children: List[QueryNode] = list()
            while len(self.stack) > pos:
                children.insert(0, self.stack.pop())

            node = ExpressionAnd(children)
            if self.parser.enableSourceLocations:
                node.location = SourceLocation.fromContext(ctx)
            self.stack.append(node)
        else:
            raise ExpressionTreeBuilderException("visitExpression_and is empty")

        LOGGER.debug("visitExpression_and/exit: stack=%s", self.stack)
        return None

    def visitAttribute(self, ctx: FCSParser.AttributeContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitAttribute/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        # handle optional qualifier
        q_ctx = ctx.qualifier()
        qualifier = q_ctx.getText() if q_ctx is not None else EMPTY_STRING

        i_ctx = ctx.identifier()
        assert i_ctx, f"ctx.identifier() must not be None in {ctx=}"
        self.stack.append(i_ctx.getText())
        self.stack.append(qualifier)

        LOGGER.debug("visitAttribute/exit: stack=%s", self.stack)
        return None

    def visitRegexp(self, ctx: FCSParser.RegexpContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitRegexp/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        p_ctx = ctx.regexp_pattern()
        assert p_ctx is not None, f"ctx.regexp_pattern() must not be None in {ctx=}"
        regex = ExpressionTreeBuilder.stripQuotes(p_ctx.getText())

        # process escape sequences, if present
        if "\\" in regex:
            regex = ExpressionTreeBuilder.unescapeString(regex)

        # perform unicode normalization, if requested
        if self.parser.unicode_normalization_form:
            regex = unicodedata.normalize(self.parser.unicode_normalization_form, regex)

        # FIXME: validate regex?
        self.stack.append(regex)

        # handle regex flags, if any
        f_ctx = ctx.regexp_flag()
        if f_ctx:
            val = f_ctx.getText()
            flags: Set[RegexFlag] = set()
            for i in range(len(val)):
                flag = val[i]
                if flag in ("i", "c"):
                    flags.add(RegexFlag.CASE_INSENSITIVE)
                elif flag in ("I", "C"):
                    flags.add(RegexFlag.CASE_SENSITIVE)
                elif flag == "l":
                    flags.add(RegexFlag.LITERAL_MATCHING)
                elif flag == "d":
                    flags.add(RegexFlag.IGNORE_DIACRITICS)
                else:
                    raise ExpressionTreeBuilderException(f"unknown regex modifier flag: {flag}")

            # validate regex flags
            if RegexFlag.CASE_SENSITIVE in flags and RegexFlag.CASE_INSENSITIVE in flags:
                raise ExpressionTreeBuilderException(
                    "invalid combination of regex modifier flags: " "'i' or 'c' and 'I' or 'C' are mutually exclusive"
                )
            if RegexFlag.LITERAL_MATCHING in flags and any(
                flag in flags
                for flag in {
                    RegexFlag.CASE_SENSITIVE,
                    RegexFlag.CASE_INSENSITIVE,
                    RegexFlag.IGNORE_DIACRITICS,
                }
            ):
                raise ExpressionTreeBuilderException(
                    "invalid combination of regex modifier flags: 'l' "
                    "is mutually exclusive with 'i', 'c', 'I', 'C' or 'd'"
                )

            self.stack.append(flags)

        else:
            # regex without flags, so push 'empty' flags on stack
            self.stack.append(set())

        LOGGER.debug("visitRegexp/exit: stack=%s", self.stack)
        return None

    def visitWithin_part_simple(self, ctx: FCSParser.Within_part_simpleContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "visitWithin_part_simple/enter: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        scope: SimpleWithinScope
        c_ctx = ctx.getChild(0)
        assert c_ctx is not None, f"ctx.getChild(0) must not be None in {ctx=}"
        val = c_ctx.getText()
        if val in ("sentence", "s"):
            scope = SimpleWithinScope.SENTENCE
        elif val in ("utterance", "u"):
            scope = SimpleWithinScope.UTTERANCE
        elif val in ("paragraph", "p"):
            scope = SimpleWithinScope.PARAGRAPH
        elif val in ("turn", "t"):
            scope = SimpleWithinScope.TURN
        elif val == "text":
            scope = SimpleWithinScope.TEXT
        elif val == "session":
            scope = SimpleWithinScope.SESSION
        else:
            raise ExpressionTreeBuilderException(f"invalid scope for simple 'within' clause: {val}")

        node = SimpleWithin(scope)
        if self.parser.enableSourceLocations:
            node.location = SourceLocation.fromContext(ctx)
        self.stack.append(node)

        LOGGER.debug("visitWithin_part_simple/exit: stack=%s", self.stack)
        return None

    # ----------------------------------------------------

    @staticmethod
    def processRepetition(ctx: FCSParser.QuantifierContext) -> Tuple[int, int]:
        if ctx.Q_ZERO_OR_MORE() is not None:  # "*"
            return REP_ZERO_OR_MORE
        if ctx.Q_ONE_OR_MORE() is not None:  # "+"
            return REP_ONE_OR_MORE
        if ctx.Q_ZERO_OR_ONE() is not None:  # "?"
            return REP_ZERO_OR_ONE
        if ctx.L_CURLY_BRACKET() is not None:  # "{x, y}" variants
            return ExpressionTreeBuilder.processRepetitionRange(ctx)

        tn: TerminalNodeImpl = ctx.getChild(0, antlr4.TerminalNode)  # type: ignore
        tok = tn.symbol if tn else None
        tok_text = tok if tok else "?"
        raise ExpressionTreeBuilderException(f"unexpected symbol in repetition quantifier: {tok_text}")

    @staticmethod
    def processRepetitionRange(ctx: FCSParser.QuantifierContext) -> Tuple[int, int]:
        comma_idx = ExpressionTreeBuilder.getChildIndex(ctx, 0, FCSParser.Q_COMMA)
        int1_idx = ExpressionTreeBuilder.getChildIndex(ctx, 0, FCSParser.INTEGER)
        int2_idx = ExpressionTreeBuilder.getChildIndex(ctx, int1_idx + 1, FCSParser.INTEGER)
        min = 0
        max = OCCURS_UNBOUNDED
        if comma_idx != -1:
            if int1_idx < comma_idx:
                min = ExpressionTreeBuilder.parseInt(ctx.getChild(int1_idx).getText())  # type: ignore
            if comma_idx < int1_idx:
                max = ExpressionTreeBuilder.parseInt(ctx.getChild(int1_idx).getText())  # type: ignore
            elif comma_idx < int2_idx:
                max = ExpressionTreeBuilder.parseInt(ctx.getChild(int2_idx).getText())  # type: ignore
        else:
            if int1_idx == -1:
                raise ExpressionTreeBuilderException("int1_idx == -1")
            min = max = ExpressionTreeBuilder.parseInt(ctx.getChild(int1_idx).getText())  # type: ignore
        if max != OCCURS_UNBOUNDED and min > max:
            raise ExpressionTreeBuilderException(f"bad qualifier: min > max ({min} > {max})")
        return (min, max)

    @staticmethod
    def getChildIndex(ctx: ParserRuleContext, start: int, ttype: int) -> int:
        if start >= 0 and start < ctx.getChildCount():
            for idx in range(start, ctx.getChildCount()):
                tree = ctx.getChild(idx)
                if isinstance(tree, antlr4.TerminalNode):
                    if tree.symbol.type == ttype:
                        return idx
        return -1

    @staticmethod
    def parseInt(val: str) -> int:
        try:
            return int(val)
        except ValueError as ex:
            raise ExpressionTreeBuilderException(f"invalid integer: {val}") from ex

    @staticmethod
    def stripQuotes(val: str) -> str:
        if val.startswith('"'):
            if val.endswith('"'):
                val = val[1:-1]
            else:
                raise ExpressionTreeBuilderException("value not properly quoted; invalid closing quote")
        elif val.startswith("'"):
            if val.endswith("'"):
                val = val[1:-1]
            else:
                raise ExpressionTreeBuilderException("value not properly quoted; invalid closing quote")
        else:
            raise ExpressionTreeBuilderException(
                "value not properly quoted; expected \" (double quote) or ' (single qoute) character"
            )
        return val

    @staticmethod
    def unescapeString(val: str) -> str:
        chars = list()
        i = 0
        while i < len(val):
            cp = val[i]
            if cp == "\\":
                i += 1  # skip slash
                cp = val[i]

                if cp == "\\":  # slash
                    chars.append("\\")
                elif cp == '"':  # double quote
                    chars.append('"')
                elif cp == "'":  # single quote
                    chars.append("'")
                elif cp == "n":  # new line
                    chars.append("\n")
                elif cp == "t":  # tabulator
                    chars.append("\t")
                elif cp == ".":  # regex: dot
                    chars.append("\\.")
                elif cp == "^":  # regex: caret
                    chars.append("\\^")
                elif cp == "$":  # regex: dollar
                    chars.append("\\$")
                elif cp == "*":  # regex: asterisk
                    chars.append("\\*")
                elif cp == "+":  # regex: plus
                    chars.append("\\+")
                elif cp == "?":  # regex: question mark
                    chars.append("\\?")
                elif cp == "(":  # regex: opening parenthesis
                    chars.append("\\(")
                elif cp == ")":  # regex: closing parenthesis
                    chars.append("\\)")
                elif cp == "{":  # regex: opening curly brace
                    chars.append("\\{")
                elif cp == "[":  # regex: opening square bracket
                    chars.append("\\[")
                elif cp == "|":  # regex: vertical bar
                    chars.append("\\|")
                elif cp == "x":  # x HEX HEX
                    chars.append(ExpressionTreeBuilder.unescapeUnicode(val, i, 2))
                    i += 2
                elif cp == "u":  # u HEX HEX HEX HEX
                    chars.append(ExpressionTreeBuilder.unescapeUnicode(val, i, 4))
                    i += 4
                elif cp == "U":  # U HEX HEX HEX HEX HEX HEX HEX HEX
                    # TODO: does this even work in python?
                    chars.append(ExpressionTreeBuilder.unescapeUnicode(val, i, 8))
                    i += 8
                else:
                    raise ExpressionTreeBuilderException(f"invalid escape sequence: \\{cp}")
            else:
                # no error should happen here (Python uses unicode by default)
                # so no back-and-forth with codepoint conversions
                chars.append(cp)
            i += 1
        return "".join(chars)

    @staticmethod
    def unescapeUnicode(val: str, i: int, size: int) -> str:
        # NOTE: or simply: `return chr(int(val[i+1:i+size+1], 16))`
        if (len(val) - i - 1) >= size:
            cp = 0  # codepoint
            for pos in range(size):
                i += 1
                if pos > 0:
                    cp <<= 4
                cp |= ExpressionTreeBuilder.parseHexChar(val[i])
            try:
                return chr(cp)
            except ValueError:
                raise ExpressionTreeBuilderException(f"invalid codepoint: U+{cp:X}")

        else:
            raise ExpressionTreeBuilderException(f"truncated escape sequence: \\{val[i]}")

    @staticmethod
    def parseHexChar(val: str) -> int:
        try:
            if len(val) != 1:
                raise ValueError("length of string should be 1 for a single character")
            return int(val, 16)
        except ValueError:
            # actually, this should never happen, as ANTLR's lexer should
            # catch illegal HEX characters
            raise ExpressionTreeBuilderException(f"invalud hex character: {val}")


class QueryParser:
    """A FCS-QL query parser that produces FCS-QL expression trees."""

    def __init__(
        self,
        *,
        default_identifier: str = DEFAULT_IDENTIFIER,
        default_operator: Operator = DEFAULT_OPERATOR,
        unicode_normalization_form: Optional[_UnicodeNormalizationForm] = DEFAULT_UNICODE_NORMALIZATION_FORM,
        enableSourceLocations: bool = False,
    ) -> None:
        """[Constructor]

        Args:
            default_identifier: the default identifier to be used for simple expressions. Defaults to `DEFAULT_IDENTIFIER`.
            default_operator: the default operator. Defaults to `DEFAULT_OPERATOR`.
            unicode_normalization_form: the Unicode normalization form to be used or ``None`` to not perform normlization. Defaults to `DEFAULT_UNICODE_NORMALIZATION_FORM`.
            enableSourceLocations: whether source locations are computed for each query node. Defaults to False.
        """  # noqa: E501
        self.default_identifier = default_identifier
        self.default_operator = default_operator
        self.unicode_normalization_form = unicode_normalization_form

        self.enableSourceLocations = enableSourceLocations
        """Whether source locations are computed for each query node."""

        self.errors: List[ErrorDetail] = list()
        """List of errors when parsing fails."""

    def parse(self, query: str) -> QueryNode:
        """Parse query.

        Args:
            query: the raw FCS-QL query

        Raises:
            QueryParserException: if an error occurred

        Returns:
            QueryNode: a FCS-QL expression tree
        """
        error_listener = ErrorListener(query)
        try:
            input_stream = InputStream(query)
            lexer = FCSLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = FCSParser(stream)

            # clear (possible) default error listeners and set our own!
            lexer.removeErrorListeners()
            parser.removeErrorListeners()
            lexer.addErrorListener(error_listener)
            parser.addErrorListener(error_listener)
            # ExceptionThrowingErrorListener ?

            # commence parsing ...
            tree: FCSParser.QueryContext = parser.query()

            if not error_listener.has_errors() and parser.getNumberOfSyntaxErrors() == 0:
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug("ANTLR parse tree: %s", tree.toStringTree(FCSParser.ruleNames))

                # now build the expression tree
                builder = ExpressionTreeBuilder(self)
                builder.visit(tree)
                node: QueryNode = builder.stack.pop()
                return node
            else:
                if LOGGER.isEnabledFor(logging.DEBUG):
                    for msg in error_listener.errors:
                        LOGGER.debug("ERROR: %s", msg)

                # FIXME: include additional error information?
                first_message = error_listener.errors[0].message if error_listener.errors else "?"
                raise QueryParserException(f"unable to parse query: {first_message}")
        except ExpressionTreeBuilderException as ex:
            raise QueryParserException(str(ex)) from ex
        except QueryParserException:
            raise
        except Exception as ex:
            raise QueryParserException("an unexpected exception occured while parsing") from ex
        finally:
            # update list of errors
            self.errors = error_listener.errors


# ---------------------------------------------------------------------------
