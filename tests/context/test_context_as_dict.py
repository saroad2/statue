from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.constants import ALIASES, ALLOWED_BY_DEFAULT, HELP, PARENT
from statue.context import Context
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
)


def case_simple_context():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context_dict = {HELP: CONTEXT_HELP_STRING1}
    return context, context_dict


def case_aliased_context():
    context = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )
    context_dict = {HELP: CONTEXT_HELP_STRING1, ALIASES: [CONTEXT2, CONTEXT3]}
    return context, context_dict


def case_context_with_parent():
    parent = Context(CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    context_dict = {HELP: CONTEXT_HELP_STRING1, PARENT: CONTEXT2}
    return context, context_dict


def case_allowed_by_default_context():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, allowed_by_default=True)
    context_dict = {HELP: CONTEXT_HELP_STRING1, ALLOWED_BY_DEFAULT: True}
    return context, context_dict


def case_full_context():
    parent = Context(CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(
        name=CONTEXT1,
        help=CONTEXT_HELP_STRING1,
        allowed_by_default=True,
        parent=parent,
        aliases=[CONTEXT3, CONTEXT4],
    )
    context_dict = {
        HELP: CONTEXT_HELP_STRING1,
        ALLOWED_BY_DEFAULT: True,
        PARENT: CONTEXT2,
        ALIASES: [CONTEXT3, CONTEXT4],
    }
    return context, context_dict


@parametrize_with_cases(argnames=["context", "context_dict"], cases=THIS_MODULE)
def test_context_as_dict(context, context_dict):
    assert context.as_dict() == context_dict
