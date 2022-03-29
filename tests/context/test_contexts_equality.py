from pytest_cases import THIS_MODULE, case, parametrize_with_cases

from statue.context import Context
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
)

EQUAL_TAG = "equal"
NOT_EQUAL_TAG = "not_equal"


# Equal cases


@case(tags=[EQUAL_TAG])
def case_equal_simple():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    return context1, context2


@case(tags=[EQUAL_TAG])
def case_equal_with_aliases():
    context1 = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )
    context2 = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )
    return context1, context2


@case(tags=[EQUAL_TAG])
def case_equal_with_parents():
    parent1 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    parent2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent1)
    context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent2)
    return context1, context2


@case(tags=[EQUAL_TAG])
def case_equal_with_allow_by_default():
    context1 = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, allowed_by_default=True
    )
    context2 = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, allowed_by_default=True
    )
    return context1, context2


# Not equal cases


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_different_name():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING1)
    return context1, context2


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_different_help():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING2)
    return context1, context2


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_different_aliases():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING2, aliases=[CONTEXT3])
    return context1, context2


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_with_different_parents():
    parent1 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    parent2 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent1)
    context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent2)
    return context1, context2


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_with_different_allow_by_default():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, allowed_by_default=True
    )
    return context1, context2


@parametrize_with_cases(
    argnames=["context1", "context2"], cases=THIS_MODULE, has_tag=EQUAL_TAG
)
def test_contexts_equality(context1, context2):
    assert context1 == context2
    assert not (context1 != context2)  # pylint: disable=superfluous-parens


@parametrize_with_cases(
    argnames=["context1", "context2"], cases=THIS_MODULE, has_tag=NOT_EQUAL_TAG
)
def test_contexts_non_equality(context1, context2):
    assert context1 != context2
    assert not (context1 == context2)  # pylint: disable=superfluous-parens
