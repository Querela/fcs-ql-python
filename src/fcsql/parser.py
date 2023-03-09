import logging
import unicodedata
from abc import ABCMeta
from abc import abstractmethod
from collections import deque
from enum import Enum
from typing import Any
from typing import Deque
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import TypeVar

import antlr4
import antlr4.error.ErrorListener
from antlr4 import CommonTokenStream
from antlr4 import InputStream
from antlr4 import ParserRuleContext
from antlr4 import ParseTreeWalker

from fcsql.FCSLexer import FCSLexer
from fcsql.FCSParser import FCSParser
from fcsql.FCSParserListener import FCSParserListener

# ---------------------------------------------------------------------------


LOGGER = logging.getLogger(__name__)


_T = TypeVar("_T", bound="QueryNode")


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


class QueryVisitor(metaclass=ABCMeta):
    """Interface implementing a Visitor pattern for FCS-QL expression trees.

    Default method implementations do nothing.
    """

    def visit(self, node: "QueryNode") -> None:
        """Visit a query node. Generic handler, dispatches to visit methods
        based on `QueryNodeType` if exists else do nothing::

            method = "visit_" + node.node_type.value

        Args:
            node: the node to visit

        Returns:
            ``None``
        """
        if not node:
            return None

        def noop(node):
            pass

        # search for specific visit function based on node_type
        method = getattr(self, f"visit_{node.node_type}", noop)

        method(node)


# ---------------------------------------------------------------------------


class QueryNode(metaclass=ABCMeta):
    """Base class for FCS-QL expression tree nodes."""

    def __init__(
        self,
        node_type: QueryNodeType,
        children: Optional[List["QueryNode"]] = None,
        child: Optional["QueryNode"] = None,
    ):
        """[Constructor]

        Args:
            node_type: the type of the node
            children: the children of this node or ``None``. Defaults to None.
            child: the child of this node or ``None``. Defaults to None.
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

    def get_child(
        self, idx: int, clazz: Optional[Type[_T]] = None
    ) -> Optional["QueryNode"]:
        """Get a child node of specified type by index.

        When supplied with ``clazz`` parameter, only child nodes of
        the requested type are counted.

        Args:
            idx: the index of the child node (if `clazz` provided, only consideres child nodes of requested type)
            clazz: the type to nodes to be considered, optional

        Returns:
            QueryNode: the child node of this node or ``None`` if not child was found (e.g. type mismatch or index out of bounds)
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

    def get_first_child(
        self, clazz: Optional[Type[_T]] = None
    ) -> Optional["QueryNode"]:
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
        return f"({self.node_type!s}{' ' + chs if chs else ''})"

    @abstractmethod
    def accept(self, visitor: QueryVisitor) -> None:
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
        parts.append(
            self.regex.translate(str.maketrans({"\n": "\\n", "\r": "\\r", "\t": "\\t"}))  # type: ignore
        )
        parts.append('"')
        if self.regex_flags:
            parts.append("/")
            # TODO: use chars from RegexFlag enum. How to guarantee same order?
            parts.append("i" if RegexFlag.CASE_INSENSITIVE in self.regex_flags else "")
            parts.append("I" if RegexFlag.CASE_SENSITIVE in self.regex_flags else "")
            parts.append("l" if RegexFlag.LITERAL_MATCHING in self.regex_flags else "")
            parts.append("d" if RegexFlag.IGNORE_DIACRITICS in self.regex_flags else "")
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
        super().__init__(
            QueryNodeType.EXPRESSION_WILDCARD, children=children, child=child
        )

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
        return f"({self.node_type!s} {self.get_first_child()!s})"

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
        ret = f"({self.node_type!s} "
        if self.min_occurs != 1:
            ret += f"@min={'*' if self.min_occurs == OCCURS_UNBOUNDED else self.min_occurs} "
        if self.max_occurs != 1:
            ret += f"@max={'*' if self.max_occurs == OCCURS_UNBOUNDED else self.max_occurs} "
        ret += f"{self.children[0]!s})"
        return ret

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
        ret = f"({self.node_type!s} "
        if self.min_occurs != 1:
            ret += f"@min={'*' if self.min_occurs == OCCURS_UNBOUNDED else self.min_occurs} "
        if self.max_occurs != 1:
            ret += f"@max={'*' if self.max_occurs == OCCURS_UNBOUNDED else self.max_occurs} "
        ret += f"{self.children[0]!s})"
        return ret

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
        return f"({self.node_type!s} {self.scope!s})"

    def accept(self, visitor: QueryVisitor) -> None:
        visitor.visit(self)


# ---------------------------------------------------------------------------


REP_ZERO_OR_MORE = (0, OCCURS_UNBOUNDED)
REP_ONE_OR_MORE = (1, OCCURS_UNBOUNDED)
REP_ZERO_OR_ONE = (0, 1)

EMPTY_STRING = ""

DEFAULT_IDENTIFIER = "text"
DEFAULT_OPERATOR = Operator.EQUALS
DEFAULT_UNICODE_NORMALIZATION_FORM = "NFC"
"""Default unicode normalization form.

See also: `unicodedata.normalize
<https://docs.python.org/3/library/unicodedata.html#unicodedata.normalize>`_
"""


# ---------------------------------------------------------------------------


class ErrorListener(antlr4.error.ErrorListener.ErrorListener):
    def __init__(self, query: str) -> None:
        super().__init__()
        self.query = query
        self.errors: List[str] = list()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # FIXME: additional information of error should not be logged but added
        # to the list of errors; that list probably needs to be enhanced to
        # store supplementary information Furthermore, a sophisticated
        # errorlist implementation could also be used by the QueryVistor to add
        # addition query error information
        if LOGGER.isEnabledFor(logging.DEBUG):
            if isinstance(offendingSymbol, antlr4.Token):
                pos = offendingSymbol.start
                if pos != -1:
                    LOGGER.debug("query: %s", self.query)
                    LOGGER.debug("       %s^- %s", " " * pos, msg)
        self.errors.append(msg)

    def has_errors(self) -> bool:
        return bool(self.errors)


class QueryParserException(Exception):
    """Query parser exception."""


class ExpressionTreeBuilderException(Exception):
    """Error building expression tree."""


class ExpressionTreeBuilder(FCSParserListener):
    def __init__(self, parser: "QueryParser") -> None:
        super().__init__()
        self.parser = parser
        self.stack: Deque[Any] = deque()
        self.stack_Query_disjunction: Deque[int] = deque()
        """for `enterQuery_disjunction`/`exitQuery_disjunction`"""
        self.stack_Query_sequence: Deque[int] = deque()
        """for `enterQuery_sequence`/`exitQuery_sequence`"""
        self.stack_Expression_or: Deque[int] = deque()
        """for `enterExpression_or`/`exitExpression_or`"""
        self.stack_Expression_and: Deque[int] = deque()
        """for `enterExpression_and`/`exitExpression_and`"""

    # ----------------------------------------------------

    def enterQuery(self, ctx: FCSParser.QueryContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterQuery: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        return super().enterQuery(ctx)

    def exitQuery(self, ctx: FCSParser.QueryContext):
        w_ctx = ctx.getChild(0, FCSParser.Within_partContext)
        if w_ctx is not None:
            within = self.stack.pop()
            query = self.stack.pop()
            self.stack.append(QueryWithWithin(query, within))

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitQuery: stack=%s", self.stack)

        return super().exitQuery(ctx)

    def enterMain_query(self, ctx: FCSParser.Main_queryContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterMain_query: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        return super().enterMain_query(ctx)

    def exitMain_query(self, ctx: FCSParser.Main_queryContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitMain_query: stack=%s", self.stack)
        return super().exitMain_query(ctx)

    def enterQuery_disjunction(self, ctx: FCSParser.Query_disjunctionContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterQuery_disjunction: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        self.stack_Query_disjunction.append(len(self.stack))
        return super().enterQuery_disjunction(ctx)

    def exitQuery_disjunction(self, ctx: FCSParser.Query_disjunctionContext):
        pos = self.stack_Query_disjunction.pop()
        if len(self.stack) > pos:
            items: List[QueryNode] = list()
            while len(self.stack) > pos:
                items.insert(0, self.stack.pop())
            self.stack.append(QueryDisjunction(items))
        else:
            raise ExpressionTreeBuilderException("exitQuery_disjunction is empty")

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitQuery_disjunction: stack=%s", self.stack)
        return super().exitQuery_disjunction(ctx)

    def enterQuery_sequence(self, ctx: FCSParser.Query_sequenceContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterQuery_sequence: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        self.stack_Query_sequence.append(len(self.stack))
        return super().enterQuery_sequence(ctx)

    def exitQuery_sequence(self, ctx: FCSParser.Query_sequenceContext):
        pos = self.stack_Query_sequence.pop()
        if len(self.stack) > pos:
            items: List[QueryNode] = list()
            while len(self.stack) > pos:
                items.insert(0, self.stack.pop())
            self.stack.append(QuerySequence(items))
        else:
            raise ExpressionTreeBuilderException("exitQuery_sequence is empty")

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitQuery_sequence: stack=%s", self.stack)
        return super().exitQuery_sequence(ctx)

    def enterQuery_group(self, ctx: FCSParser.Query_groupContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterQuery_group: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        return super().enterQuery_group(ctx)

    def exitQuery_group(self, ctx: FCSParser.Query_groupContext):
        # handle repetition (if any)
        min = max = 1

        # fetch *first* child of type QuantifierContext, therefore idx=0
        q_ctx = ctx.getChild(0, FCSParser.QualifierContext)
        if q_ctx is not None:
            min, max = ExpressionTreeBuilder.processRepetition(ctx)

        content: QueryNode = self.stack.pop()
        self.stack.append(QueryGroup(content, min, max))

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitQuery_group: stack=%s", self.stack)
        return super().exitQuery_group(ctx)

    def enterQuery_simple(self, ctx: FCSParser.Query_simpleContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterQuery_simple: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        return super().enterQuery_simple(ctx)

    def exitQuery_simple(self, ctx: FCSParser.Query_simpleContext):
        # handle repetition (if any)
        min = max = 1

        # fetch *first* child of type QuantifierContext, therefore idx=0
        q_ctx = ctx.getChild(0, FCSParser.QualifierContext)
        if q_ctx is not None:
            min, max = ExpressionTreeBuilder.processRepetition(ctx)

        expression: QueryNode = self.stack.pop()
        self.stack.append(QuerySegment(expression, min, max))

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitQuery_simple: stack=%s", self.stack)
        return super().exitQuery_simple(ctx)

    def enterQuery_implicit(self, ctx: FCSParser.Query_implicitContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterQuery_implicit: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        self.stack.append(self.parser.default_operator)
        self.stack.append(self.parser.default_identifier)
        self.stack.append(EMPTY_STRING)
        return super().enterQuery_implicit(ctx)

    def exitQuery_implicit(self, ctx: FCSParser.Query_implicitContext):
        regex_flags: Set[RegexFlag] = self.stack.pop()
        regex_value: str = self.stack.pop()
        qualifier: str = self.stack.pop()
        identifier: str = self.stack.pop()
        operator: Operator = self.stack.pop()

        self.stack.append(
            Expression(
                qualifier=qualifier,
                identifier=identifier,
                operator=operator,
                regex=regex_value,
                regex_flags=regex_flags,
            )
        )

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitQuery_implicit: stack=%s", self.stack)
        return super().exitQuery_implicit(ctx)

    # TODO: check, abortable, if also exit?
    def enterQuery_segment(self, ctx: FCSParser.Query_segmentContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterQuery_segment: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        # if the context contains only two children, they must be
        # '[' and ']' thus we are dealing with a wildcard segment
        if ctx.getChildCount() == 2:
            self.stack.append(ExpressionWildcard())

        # TODO: not exactly matching the java implementation
        # do we need to block 'visitQuery_segment' call?

        return super().enterQuery_segment(ctx)

    def exitQuery_segment(self, ctx: FCSParser.Query_segmentContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitQuery_segment: stack=%s", self.stack)
        return super().exitQuery_segment(ctx)

    def enterExpression_basic(self, ctx: FCSParser.Expression_basicContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterExpression_basic: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        tok_op = ctx.getChild(1).symbol
        if tok_op.type == FCSLexer.OPERATOR_EQ:
            self.stack.append(Operator.EQUALS)
        elif tok_op.type == FCSLexer.OPERATOR_NE:
            self.stack.append(Operator.NOT_EQUALS)
        else:
            raise ExpressionTreeBuilderException(
                f"invalid operator type: {tok_op.text}"
            )

        return super().enterExpression_basic(ctx)

    def exitExpression_basic(self, ctx: FCSParser.Expression_basicContext):
        regex_flags: Set[RegexFlag] = self.stack.pop()
        regex_value: str = self.stack.pop()
        qualifier: str = self.stack.pop()
        identifier: str = self.stack.pop()
        operator: Operator = self.stack.pop()

        self.stack.append(
            Expression(
                qualifier=qualifier,
                identifier=identifier,
                operator=operator,
                regex=regex_value,
                regex_flags=regex_flags,
            )
        )

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitExpression_basic: stack=%s", self.stack)
        return super().exitExpression_basic(ctx)

    def enterExpression_not(self, ctx: FCSParser.Expression_notContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterExpression_not: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        return super().enterExpression_not(ctx)

    def exitExpression_not(self, ctx: FCSParser.Expression_notContext):
        expression: QueryNode = self.stack.pop()
        self.stack.append(ExpressionNot(expression))

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitExpression_not: stack=%s", self.stack)
        return super().exitExpression_not(ctx)

    def enterExpression_group(self, ctx: FCSParser.Expression_groupContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterExpression_group: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        return super().enterExpression_group(ctx)

    def exitExpression_group(self, ctx: FCSParser.Expression_groupContext):
        expression: QueryNode = self.stack.pop()
        self.stack.append(ExpressionGroup(expression))

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitExpression_group: stack=%s", self.stack)
        return super().exitExpression_group(ctx)

    def enterExpression_or(self, ctx: FCSParser.Expression_orContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterExpression_or: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        self.stack_Expression_or.append(len(self.stack))
        return super().enterExpression_or(ctx)

    def exitExpression_or(self, ctx: FCSParser.Expression_orContext):
        pos = self.stack_Expression_or.pop()
        if len(self.stack) > pos:
            children: List[QueryNode] = list()
            while len(self.stack) > pos:
                children.insert(0, self.stack.pop())
            self.stack.append(ExpressionOr(children))
        else:
            raise ExpressionTreeBuilderException("exitExpression_or is empty")

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitExpression_or: stack=%s", self.stack)
        return super().exitExpression_or(ctx)

    def enterExpression_and(self, ctx: FCSParser.Expression_andContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterExpression_and: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )
        self.stack_Expression_and.append(len(self.stack))
        return super().enterExpression_and(ctx)

    def exitExpression_and(self, ctx: FCSParser.Expression_andContext):
        pos = self.stack_Expression_and.pop()
        if len(self.stack) > pos:
            children: List[QueryNode] = list()
            while len(self.stack) > pos:
                children.insert(0, self.stack.pop())
            self.stack.append(ExpressionAnd(children))
        else:
            raise ExpressionTreeBuilderException("exitExpression_and is empty")

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitExpression_and: stack=%s", self.stack)
        return super().exitExpression_and(ctx)

    # TODO: check, or exit
    def enterAttribute(self, ctx: FCSParser.AttributeContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterAttribute: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        # handle optional qualifier
        q_ctx = ctx.getChild(0, FCSParser.QualifierContext)
        qualifier = q_ctx.getText() if q_ctx is not None else EMPTY_STRING

        self.stack.append(ctx.getChild(0, FCSParser.IdentifierContext).getText())
        self.stack.append(qualifier)

        return super().enterAttribute(ctx)

    def exitAttribute(self, ctx: FCSParser.AttributeContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitAttribute: stack=%s", self.stack)
        return super().exitAttribute(ctx)

    # TODO: check, or exit
    def enterRegexp(self, ctx: FCSParser.RegexpContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterRegexp: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        p_ctx = ctx.getChild(0, FCSParser.Regexp_patternContext)
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
        f_ctx = ctx.getChild(0, FCSParser.Regexp_flagContext)
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
                    raise ExpressionTreeBuilderException(
                        f"unknown regex modifier flag: {flag}"
                    )

            # validate regex flags
            if (
                RegexFlag.CASE_SENSITIVE in flags
                and RegexFlag.CASE_INSENSITIVE in RegexFlag.CASE_SENSITIVE
            ):
                raise ExpressionTreeBuilderException(
                    "invalid combination of regex modifier flags: "
                    "'i' or 'c' and 'I' or 'C' are mutually exclusive"
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

        return super().enterRegexp(ctx)

    def exitRegexp(self, ctx: FCSParser.RegexpContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitRegexp: stack=%s", self.stack)
        return super().exitRegexp(ctx)

    # TODO: check, abortable, if also exit?
    def enterWithin_part_simple(self, ctx: FCSParser.Within_part_simpleContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "enterWithin_part_simple: children=%s / cnt=%s / text=%s",
                ctx.children,
                ctx.getChildCount(),
                ctx.getText(),
            )

        scope: SimpleWithinScope
        val = ctx.getChild(0).getText()
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
            raise ExpressionTreeBuilderException(
                f"invalid scope for simple 'within' clause: {val}"
            )

        self.stack.append(SimpleWithin(scope))

        return super().enterWithin_part_simple(ctx)

    def exitWithin_part_simple(self, ctx: FCSParser.Within_part_simpleContext):
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug("exitWithin_part_simple: stack=%s", self.stack)
        return super().exitWithin_part_simple(ctx)

    # ----------------------------------------------------

    @staticmethod
    def processRepetition(ctx: FCSParser.QualifierContext) -> Tuple[int, int]:
        tok: antlr4.Token = ctx.getChild(0, antlr4.TerminalNode).symbol
        if tok.type == FCSParser.Q_ZERO_OR_MORE:  # "*"
            return REP_ZERO_OR_MORE
        if tok.type == FCSParser.Q_ONE_OR_MORE:  # "+"
            return REP_ONE_OR_MORE
        if tok.type == FCSParser.Q_ZERO_OR_ONE:  # "?"
            return REP_ZERO_OR_ONE
        if tok.type == FCSParser.L_CURLY_BRACKET:  # "{x, y}" variants
            return ExpressionTreeBuilder.processRepetitionRange(ctx)
        raise ExpressionTreeBuilderException(
            f"unexpected symbol in repetition quantifier: {tok.text}"
        )

    @staticmethod
    def processRepetitionRange(ctx: FCSParser.QuantifierContext) -> Tuple[int, int]:
        comma_idx = ExpressionTreeBuilder.getChildIndex(ctx, 0, FCSParser.Q_COMMA)
        int1_idx = ExpressionTreeBuilder.getChildIndex(ctx, 0, FCSParser.INTEGER)
        int2_idx = ExpressionTreeBuilder.getChildIndex(
            ctx, int1_idx + 1, FCSParser.INTEGER
        )
        min = 0
        max = OCCURS_UNBOUNDED
        if comma_idx != -1:
            if int1_idx < comma_idx:
                min = ExpressionTreeBuilder.parseInt(ctx.getChild(int1_idx).getText())
            if comma_idx < int1_idx:
                max = ExpressionTreeBuilder.parseInt(ctx.getChild(int1_idx).getText())
            elif comma_idx < int2_idx:
                max = ExpressionTreeBuilder.parseInt(ctx.getChild(int2_idx).getText())
        else:
            if int1_idx == -1:
                raise ExpressionTreeBuilderException("int1_idx == -1")
            min = max = ExpressionTreeBuilder.parseInt(ctx.getChild(int1_idx).getText())
        if max != OCCURS_UNBOUNDED and min > max:
            raise ExpressionTreeBuilderException(
                f"bad qualifier: min > max ({min} > {max})"
            )
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
                raise ExpressionTreeBuilderException(
                    "value not properly quoted; invalid closing quote"
                )
        elif val.startswith("'"):
            if val.endswith("'"):
                val = val[1:-1]
            else:
                raise ExpressionTreeBuilderException(
                    "value not properly quoted; invalid closing quote"
                )
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
                    raise ExpressionTreeBuilderException(
                        f"invalid escape sequence: \\{cp}"
                    )
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
            raise ExpressionTreeBuilderException(
                f"truncated escape sequence: \\{val[i]}"
            )

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
        default_identifier: str = DEFAULT_IDENTIFIER,
        default_operator: Operator = DEFAULT_OPERATOR,
        unicode_normalization_form: Optional[str] = DEFAULT_UNICODE_NORMALIZATION_FORM,
    ) -> None:
        """[Constructor]

        Args:
            default_identifier: the default identifier to be used for simple expressions. Defaults to `DEFAULT_IDENTIFIER`.
            default_operator: the default operator. Defaults to `DEFAULT_OPERATOR`.
            unicode_normalization_form: the Unicode normalization form to be used or ``None`` to not perform normlization. Defaults to `DEFAULT_UNICODE_NORMALIZATION_FORM`.
        """  # noqa: E501
        self.default_identifier = default_identifier
        self.default_operator = default_operator
        self.unicode_normalization_form = unicode_normalization_form

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

            if (
                not error_listener.has_errors()
                and parser.getNumberOfSyntaxErrors() == 0
            ):
                if LOGGER.isEnabledFor(logging.DEBUG):
                    LOGGER.debug(
                        "ANTLR parse tree: %s", tree.toStringTree(FCSParser.ruleNames)
                    )

                # now build the expression tree
                builder = ExpressionTreeBuilder(self)
                walker = ParseTreeWalker()
                walker.walk(builder, tree)
                return builder.stack.pop()
            else:
                if LOGGER.isEnabledFor(logging.DEBUG):
                    for msg in error_listener.errors:
                        LOGGER.debug("ERROR: %s", msg)

                # FIXME: (include additional error information)
                raise QueryParserException(
                    (error_listener.errors or ["unspecified error"])[0]
                )
        except ExpressionTreeBuilderException as ex:
            raise QueryParserException(str(ex)) from ex
        except QueryParserException:
            raise
        except Exception as ex:
            raise QueryParserException(
                "an unexpected exception occured while parsing"
            ) from ex


# ---------------------------------------------------------------------------
