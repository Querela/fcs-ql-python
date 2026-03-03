import pytest

from fcsql import validate
from fcsql.parser import QueryParser
from fcsql.parser import SourceLocation
from fcsql.validation import FCSQLValidator
from fcsql.validation import SpecificationValidationError

# ---------------------------------------------------------------------------


@pytest.fixture
def parser():
    """Query Parser with ``SourceLocation``s enabled.

    Returns:
        QueryParser: the query parser for parsing query strings
    """
    return QueryParser(enableSourceLocations=True)


# ---------------------------------------------------------------------------
# test convenience validate method


def test_validate():
    # valid queries
    assert validate('"Banane"') is True
    assert validate('[ text = "Banane" ]') is True
    assert validate('[text="Banane"] ') is True
    assert validate("[]") is True
    assert validate('[ pos = "NOUN" ]{2,}') is True

    # invalid (parse error)
    assert validate("") is False
    assert validate("[ ") is False
    # invalid (invalid layer)
    assert validate('[ test = "Banane" ]') is False

    # with specific version number
    assert validate('[pos = "NOUN"]', version="2.2") is True
    # invalid version number raises
    with pytest.raises(ValueError):
        validate("[]", version="1.0")


def test_validate_with_errors_list():
    # valid queries
    assert len(validate("[]", return_errors=True)) == 0

    # invalid queries (parse error)
    errors = validate("[", return_errors=True)
    assert len(errors) == 1
    assert errors[0].fragment == "["
    # indicates end of string (missing something)
    assert errors[0].position == SourceLocation(start=1, stop=1)
    assert errors[0].message == """no viable alternative at input '['"""

    # invalid queries (validation error)
    errors = validate('[post = "NOUN"]', return_errors=True)
    assert len(errors) == 1
    assert errors[0].fragment == 'post = "NOUN"'
    assert errors[0].position == SourceLocation(start=1, stop=14)  # inner expression
    assert errors[0].message == "Unknown layer identifier 'post'!"


def test_validate_with_warnings_list():
    # "valid" queries (warnings are ok)
    # but if warnings are handled as errors, we have something returned
    pass


# ---------------------------------------------------------------------------
# test for FCS(-QL) v2.2


def test_validation_basic_v2_2(parser: QueryParser):
    query = '"Banane"'
    node = parser.parse(query)

    validator = FCSQLValidator()
    assert validator.query is None

    validator.validate(node, query=query)
    assert validator.query == query
    assert not validator.errors

    # create validator with a query string (which might not be the real one)
    validator = FCSQLValidator(query="test")
    assert validator.query == "test"
    # the query will be overwritten in the .validate() method
    validator.validate(node, query=query)
    assert validator.query == query
    assert not validator.errors

    # repeated calls should reset correctly
    validator.validate(node, query=query)
    assert validator.query == query
    assert not validator.errors

    # convenience method
    assert validator.is_valid(node) is True
    assert validator.query == query
    assert not validator.errors


def test_validation_violation_basic_v2_2(parser: QueryParser):
    query = """[ lemmas = "invalid" ]"""
    node = parser.parse(query)

    # fail on first violation
    validator = FCSQLValidator(raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match(r"Unknown layer identifier 'lemmas'!")
    assert exc.value.query_fragment == 'lemmas = "invalid"'

    # or we can record violations
    validator = FCSQLValidator(raise_at_first_violation=False)
    is_valid = validator.validate(node, query=query)
    assert is_valid is False
    assert len(validator.errors) == 1
    assert validator.errors[0].fragment == 'lemmas = "invalid"'

    # reset .errors list
    is_valid = validator.validate(node, query=query)
    assert is_valid is False
    assert len(validator.errors) == 1


def test_validation_violation_multiple_v2_2(parser: QueryParser):
    query = """[ post = "NOUN"] [lemmas = "der"]"""
    node = parser.parse(query)

    validator = FCSQLValidator(raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match(r"Unknown layer identifier 'post'!")
    assert exc.value.query_fragment == 'post = "NOUN"'
    assert len(validator.errors) == 0

    validator = FCSQLValidator(raise_at_first_violation=False)
    is_valid = validator.validate(node, query=query)
    assert is_valid is False
    assert len(validator.errors) == 2
    assert validator.errors[0].message == "Unknown layer identifier 'post'!"
    assert validator.errors[0].fragment == 'post = "NOUN"'
    assert validator.errors[1].message == "Unknown layer identifier 'lemmas'!"
    assert validator.errors[1].fragment == 'lemmas = "der"'


def test_validation_custom_layer_v2_2(parser: QueryParser):
    query = """[ post = "NOUN"]"""
    node = parser.parse(query)

    validator = FCSQLValidator(raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match(r"Unknown layer identifier 'post'!")
    assert exc.value.query_fragment == 'post = "NOUN"'
    assert len(validator.errors) == 0

    # "post" is a custom layer, so allowed
    validator = FCSQLValidator(allowed_layer_identifiers=["post"], raise_at_first_violation=True)
    assert validator.validate(node, query=query) is True

    # but not if something else
    validator = FCSQLValidator(allowed_layer_identifiers=["lemmas"], raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match(r"Unknown layer identifier 'post' \(only allowed: \['lemmas'\]\)!")
    assert exc.value.query_fragment == 'post = "NOUN"'
    assert len(validator.errors) == 0


def test_validation_custom_layer_qualifiers_v2_2(parser: QueryParser):
    query = """[ stts:pos = "NNS"]"""
    node = parser.parse(query)

    # by default layer qualifiers are ok
    validator = FCSQLValidator(raise_at_first_violation=True)
    assert validator.validate(node, query=query) is True

    # but we can restrict, either none are allowed
    validator = FCSQLValidator(allowed_layer_qualifiers=[("pos", None)], raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match(r"Usage of layer qualifier 'stts' which is not allowed for layer with identifier 'pos'!")

    # or some
    validator = FCSQLValidator(allowed_layer_qualifiers=[("pos", ["ud17", "xyz"])], raise_at_first_violation=True)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match(
        r"Usage of unknown layer qualifier 'stts' for layer with identifier 'pos' \(only allowed: \['ud17', 'xyz'\]\)!"
    )

    # or some with our custom included
    validator = FCSQLValidator(allowed_layer_qualifiers=[("pos", ["ud17", "stts"])], raise_at_first_violation=True)
    assert validator.validate(node, query=query) is True

    # ------------------------------------------

    # it can still fail if the layer is not allowed!
    # but it will only output the error where it is
    validator = FCSQLValidator(
        allowed_layer_identifiers=["abc"],
        allowed_layer_qualifiers=[("pos", ["ud17", "stts"])],
        raise_at_first_violation=False,
    )
    validator.validate(node, query=query)
    assert len(validator.errors) == 1
    assert validator.errors[0].message == "Unknown layer identifier 'pos' (only allowed: ['abc'])!"


def test_is_likely_a_regex():
    from fcsql.validation import is_likely_a_regex

    assert is_likely_a_regex("NOUN") is False
    assert is_likely_a_regex("multiple words") is False

    assert is_likely_a_regex("^NOUN") is True
    assert is_likely_a_regex("NOUN$") is True
    assert is_likely_a_regex("NOUN?") is True
    assert is_likely_a_regex("(NOUN)") is True
    assert is_likely_a_regex("N[O]UN") is True

    assert is_likely_a_regex("with\\ escapes") is True

    # false positives
    assert is_likely_a_regex("test.") is True
    assert is_likely_a_regex("test?") is True


def test_validation_errors_warnings_reset(parser: QueryParser):
    query = """[ pos = "NNS"]"""
    node = parser.parse(query)

    # if only as a warning, then validates ok
    validator = FCSQLValidator(raise_at_first_violation=False, warnings_as_errors=False)
    assert validator.validate(node, query=query) is True
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 1

    # if warnings are errors, then it fails validation
    validator = FCSQLValidator(raise_at_first_violation=False, warnings_as_errors=True)
    assert validator.validate(node, query=query) is False
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 1

    # just a test to check it resets properly
    assert validator.validate(node, query=query) is False
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 1

    # again, same but different
    query = """[ post = "NNS"]"""
    node = parser.parse(query)
    assert validator.validate(node, query=query) is False
    assert len(validator.errors) == 1
    assert len(validator.warnings) == 0


def test_validation_pos_layer_v2_2(parser: QueryParser):
    query = """[ stts:pos = "NNS"]"""
    node = parser.parse(query)
    validator = FCSQLValidator(raise_at_first_violation=True, warnings_as_errors=True)
    validator.validate(node, query=query)

    query = """[ pos = "NNS"]"""
    node = parser.parse(query)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)
    assert exc.match(
        r"Layer 'pos' without qualifier should use UD17 POS tags, found 'NNS' "
        r"\(recommended to only use: \['ADJ', 'ADV', 'INTJ', 'NOUN', 'PROPN', 'VERB', 'ADP', 'AUX',"
        r" 'CCONJ', 'DET', 'NUM', 'PART', 'PRON', 'SCONJ', 'PUNCT', 'SYM', 'X'\]\)"
    )

    query = """[ pos = "ART"]"""
    node = parser.parse(query)
    with pytest.raises(SpecificationValidationError) as exc:
        validator.validate(node, query=query)


def test_validation_word_layer(parser: QueryParser):
    query = """[ word = "test" ]"""
    node = parser.parse(query)

    validator = FCSQLValidator(raise_at_first_violation=False, warnings_as_errors=False)
    assert validator.validate(node, query=query) is True
    assert len(validator.errors) == 0
    assert len(validator.warnings) == 1
    assert validator.warnings[0].message == "Usage of legacy(?) layer 'word'. Did you mean 'text' instead?"
    assert validator.warnings[0].fragment == 'word = "test"'


# ---------------------------------------------------------------------------
