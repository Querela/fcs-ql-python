import logging
from abc import ABCMeta
from collections import deque
from typing import Deque
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import Union

from fcsql.parser import ErrorDetail
from fcsql.parser import Expression
from fcsql.parser import ExpressionAnd
from fcsql.parser import ExpressionGroup
from fcsql.parser import ExpressionNot
from fcsql.parser import ExpressionOr
from fcsql.parser import ExpressionWildcard
from fcsql.parser import QueryDisjunction
from fcsql.parser import QueryGroup
from fcsql.parser import QueryNode
from fcsql.parser import QuerySegment
from fcsql.parser import QuerySequence
from fcsql.parser import QueryVisitorAdapter
from fcsql.parser import QueryWithWithin
from fcsql.parser import SimpleWithin

# ---------------------------------------------------------------------------

LOGGER = logging.getLogger(__name__)

_R = TypeVar("_R")

# ---------------------------------------------------------------------------


class SpecificationValidationError(Exception):
    def __init__(self, msg: str, node: QueryNode, query_fragment: Optional[str] = None, *args):
        super().__init__(msg, *args)
        self.node = node
        self.query_fragment = query_fragment


class Validator(QueryVisitorAdapter[_R], metaclass=ABCMeta):
    """An abstract base Validator for FCS-QL queries.

    Subclasses should override the ``visit_`` QueryNode methods to
    implement the validation logic and use the ``.validation_error()``
    to raise/track validation errors and ``.validation_warning()`` for
    warnings (may also raise errors depending on configuration).
    """

    def __init__(
        self,
        *,
        query: Optional[str] = None,
        raise_at_first_violation: bool = True,
        warnings_as_errors: bool = False,
    ):
        """Creates a FCS-QL Validator that checks that only known indexes are used
        and that relations and relation modifiers are valid.

        Args:
            query: the original query string used for constructing the query node tree.
                   Used to provide more context for validation errors. Defaults to None.
            raise_at_first_violation: Raise a ``SpecificationValidationError`` at first
                                      conformance validation or try to gather as many infos
                                      as possible. Will be available in ``.errors`` attribute.
                                      Defaults to True.
            warnings_as_errors: Handle warnings the same as errors. May raise ``SpecificationValidationError``.
        """
        super().__init__()

        self.stack: Deque[QueryNode] = deque()
        """(internal) Query node stack to keep track of query node parents."""

        self.query = query
        """query string to add context to error messages for better error locations"""

        self.raise_at_first_violation = raise_at_first_violation
        """Whether to raise at first violation."""
        self.warnings_as_errors = warnings_as_errors
        """Whether to handle warnings the same as errors."""
        self.errors: List[ErrorDetail] = list()
        """List of specification validation errors if ``.raise_at_first_violation`` is ``False``"""
        self.warnings: List[ErrorDetail] = list()
        """List of warnings about not-quite-violations of the specification but bad practice or
        what can be unexpected results."""

    def validate(self, node: QueryNode, *, query: Optional[str] = None):
        """Validate parse query node tree.

        Args:
            node: the parsed query node (root of parse tree)
            query: the raw query input string. Will be used to add more context
                   to error messages by adding the fragment where the error was
                   caused. Defaults to None.

        Returns:
            bool: ``True`` if query in valid, ``False`` if any error was recorded
                  in the ``.errors`` attribute
        """
        # allows to override the query string here
        if query is not None:
            self.query = query

        # reset list of errors
        self.errors = []
        self.warnings = []

        # start validation
        self.visit(node)

        return len(self.errors) == 0

    def is_valid(self, node: QueryNode, *, query: Optional[str] = None) -> bool:
        """Convenience method that simply calls ``.validate()`` and returns
        ``True`` if the query was valid.

        Args:
            node: the parsed query node (root of parse tree)
            query: the raw query input string. Will be used to add more context
                   to error messages by adding the fragment where the error was
                   caused. Defaults to None.

        Returns:
            bool: ``True`` if query in valid, ``False`` otherwise

        Note:
            The ``.errors`` attribute will not be used here as the first validation
            error will abort the validation process.
        """
        try:
            return self.validate(node, query=query)
        except SpecificationValidationError:
            return False

    def validation_error(self, node: QueryNode, message: str):
        """(Internal) Raises or tracks a new validation error.

        Args:
            node: the query node where the validation error was caused
            message: the error message

        Raises:
            SpecificationValidationError: the raised error if ``.raise_at_first_violation``
                                          is set to ``True``
        """
        fragment = None
        if self.query and node.location:
            fragment = self.query[node.location.start : node.location.stop]  # noqa: E203

        if self.raise_at_first_violation:
            raise SpecificationValidationError(message, node, fragment)

        self.errors.append(
            ErrorDetail(
                message=message,
                type="validation-error",
                position=node.location,
                fragment=fragment,
            )
        )

    def validation_warning(self, node: QueryNode, message: str):
        """(Internal) Tracks validation warnings.

        If ``.warnings_as_errors`` is ``True`` and ``.raise_at_first_violation``
        is ``True``, it will raise ``SpecificationValidationError``.

        Args:
            node: the query node where the validation error was caused
            message: the error message

        Raises:
            SpecificationValidationError: the raised error if ``.raise_at_first_violation``
                                          and ``.warnings_as_errors`` are set to ``True``
        """
        fragment = None
        if self.query and node.location:
            fragment = self.query[node.location.start : node.location.stop]  # noqa: E203

        if self.warnings_as_errors:
            if self.raise_at_first_violation:
                raise SpecificationValidationError(message, node, fragment)

        self.warnings.append(
            ErrorDetail(
                message=message,
                type="validation-warning",
                position=node.location,
                fragment=fragment,
            )
        )

    # ----------------------------------------------------

    @property
    def parent_node(self) -> Optional[QueryNode]:
        """Get the current parent ``QueryNode`` or ``None`` if unavailable.

        Intended to be used in the ``visit_`` ``QueryNode`` handlers.

        Returns:
            Optional[QueryNode]: the parent query node or ``None``
        """
        if self.stack:
            return self.stack[-1]
        return None

    def visit_Expression(self, node: Expression) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_Expression(node)
        self.stack.pop()
        return result

    def visit_ExpressionWildcard(self, node: ExpressionWildcard) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_ExpressionWildcard(node)
        self.stack.pop()
        return result

    def visit_ExpressionGroup(self, node: ExpressionGroup) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_ExpressionGroup(node)
        self.stack.pop()
        return result

    def visit_ExpressionNot(self, node: ExpressionNot) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_ExpressionNot(node)
        self.stack.pop()
        return result

    def visit_ExpressionAnd(self, node: ExpressionAnd) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_ExpressionAnd(node)
        self.stack.pop()
        return result

    def visit_ExpressionOr(self, node: ExpressionOr) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_ExpressionOr(node)
        self.stack.pop()
        return result

    def visit_QueryDisjunction(self, node: QueryDisjunction) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_QueryDisjunction(node)
        self.stack.pop()
        return result

    def visit_QuerySequence(self, node: QuerySequence) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_QuerySequence(node)
        self.stack.pop()
        return result

    def visit_QueryWithWithin(self, node: QueryWithWithin) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_QueryWithWithin(node)
        self.stack.pop()
        return result

    def visit_QuerySegment(self, node: QuerySegment) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_QuerySegment(node)
        self.stack.pop()
        return result

    def visit_QueryGroup(self, node: QueryGroup) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_QueryGroup(node)
        self.stack.pop()
        return result

    def visit_SimpleWithin(self, node: SimpleWithin) -> Optional[_R]:
        self.stack.append(node)
        result = super().visit_SimpleWithin(node)
        self.stack.pop()
        return result


# ---------------------------------------------------------------------------


class FCSQLValidator(Validator[None]):
    """FCS-QL Query Validator for FCS Spec 2.2"""

    SPECIFICATION_VERSION = "2.2"
    """FCS (FCS-QL) specification version"""

    KNOWN_LAYER_IDENTIFIERS = [
        "text",
        "lemma",
        "pos",
        "orth",
        "norm",
        "phonetic",
    ]

    def __init__(
        self,
        *,
        allowed_layer_identifiers: Optional[List[str]] = None,
        allowed_layer_qualifiers: Optional[List[Union[Tuple[str, None], Tuple[str, List[str]]]]] = None,
        query: Optional[str] = None,
        raise_at_first_violation: bool = True,
        warnings_as_errors: bool = False,
    ):
        super().__init__(
            query=query,
            raise_at_first_violation=raise_at_first_violation,
            warnings_as_errors=warnings_as_errors,
        )

        self.allowed_layer_identifiers = allowed_layer_identifiers
        self.allowed_layer_qualifiers = allowed_layer_qualifiers

    # ----------------------------------------------------

    def visit_Expression(self, node: Expression):
        if self.allowed_layer_identifiers:
            if node.identifier not in self.allowed_layer_identifiers:
                self.validation_error(
                    node,
                    f"Unknown layer identifier '{node.identifier}' (only allowed: {self.allowed_layer_identifiers!r})!",
                )
        else:
            if node.identifier not in self.KNOWN_LAYER_IDENTIFIERS:
                if not node.identifier.startswith("x-"):
                    self.validation_error(node, f"Unknown layer identifier '{node.identifier}'!")
                else:
                    self.validation_warning(node, f"Usage of custom layer with identifier '{node.identifier}'")

        if node.qualifier and self.allowed_layer_qualifiers:
            allowed_qualifiers = None
            for identifier, qualifiers in self.allowed_layer_qualifiers:
                if identifier == node.identifier:
                    allowed_qualifiers = qualifiers
                    break

            if allowed_qualifiers is None:
                self.validation_error(
                    node,
                    (
                        f"Usage of layer qualifier '{node.qualifier}' which is not allowed"
                        f" for layer with identifier '{node.identifier}'!"
                    ),
                )
            elif node.qualifier not in allowed_qualifiers:
                self.validation_error(
                    node,
                    (
                        f"Usage of unknown layer qualifier '{node.qualifier}' for layer with "
                        f"identifier '{node.identifier}' (only allowed: {allowed_qualifiers!r})!"
                    ),
                )

        return super().visit_Expression(node)


# ---------------------------------------------------------------------------

VALIDATORS: Dict[str, Type[Validator]] = {
    FCSQLValidator.SPECIFICATION_VERSION: FCSQLValidator,
}
"""Mapping of all known FCS-QL Validators. Uses the FCS specification
version as the key and returns the ``Validator`` class for instantiating."""

DEFAULT_VALIDATOR_SPECIFICATION_VERSION = FCSQLValidator.SPECIFICATION_VERSION
"""The default FCS specification version for FCS-QL query validation."""

# ---------------------------------------------------------------------------
