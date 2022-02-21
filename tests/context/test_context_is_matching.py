import enum

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.context import Context
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT5,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
)


class MatchEnum(enum.Enum):
    MATCH = enum.auto()
    MATCH_RECURSIVELY = enum.auto()
    NO_MATCH = enum.auto()


def case_context_is_matching_by_name():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)

    return context, MatchEnum.MATCH


def case_context_is_matching_by_first_alias():
    context = Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT1, CONTEXT3]
    )

    return context, MatchEnum.MATCH


def case_context_is_matching_by_second_alias():
    context = Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT3, CONTEXT1]
    )

    return context, MatchEnum.MATCH


def case_context_is_not_matching():
    context = Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT3, CONTEXT4]
    )

    return context, MatchEnum.NO_MATCH


def case_context_is_matching_parent_name():
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=parent)

    return context, MatchEnum.MATCH_RECURSIVELY


def case_context_is_matching_parent_first_alias():
    parent = Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT1, CONTEXT3]
    )
    context = Context(name=CONTEXT4, help=CONTEXT_HELP_STRING2, parent=parent)

    return context, MatchEnum.MATCH_RECURSIVELY


def case_context_is_matching_parent_second_alias():
    parent = Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT3, CONTEXT1]
    )
    context = Context(name=CONTEXT4, help=CONTEXT_HELP_STRING2, parent=parent)

    return context, MatchEnum.MATCH_RECURSIVELY


def case_context_is_not_matching_parent():
    parent = Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT3, CONTEXT4]
    )
    context = Context(name=CONTEXT5, help=CONTEXT_HELP_STRING2, parent=parent)

    return context, MatchEnum.NO_MATCH


def case_context_is_matching_grandparent_name():
    grandparent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=grandparent)
    context = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3, parent=parent)

    return context, MatchEnum.MATCH_RECURSIVELY


def case_context_is_not_matching_grandparent():
    grandparent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING1)
    parent = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING2, parent=grandparent)
    context = Context(name=CONTEXT4, help=CONTEXT_HELP_STRING3, parent=parent)

    return context, MatchEnum.NO_MATCH


@parametrize_with_cases(argnames=["context", "match_enum"], cases=THIS_MODULE)
def test_context_is_matching(context, match_enum):
    if match_enum == MatchEnum.MATCH:
        assert context.is_matching(CONTEXT1)
        assert context.is_matching_recursively(CONTEXT1)
    if match_enum == MatchEnum.MATCH_RECURSIVELY:
        assert not context.is_matching(CONTEXT1)
        assert context.is_matching_recursively(CONTEXT1)
    if match_enum == MatchEnum.NO_MATCH:
        assert not context.is_matching(CONTEXT1)
        assert not context.is_matching_recursively(CONTEXT1)
