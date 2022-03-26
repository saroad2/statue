from collections import OrderedDict

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
    context_dict = OrderedDict([(HELP, CONTEXT_HELP_STRING1)])
    return context, context_dict


def case_aliased_context():
    context = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )
    context_dict = OrderedDict(
        [(HELP, CONTEXT_HELP_STRING1), (ALIASES, [CONTEXT2, CONTEXT3])]
    )
    return context, context_dict


def case_context_with_parent():
    parent = Context(CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    context_dict = OrderedDict([(HELP, CONTEXT_HELP_STRING1), (PARENT, CONTEXT2)])
    return context, context_dict


def case_allowed_by_default_context():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, allowed_by_default=True)
    context_dict = OrderedDict(
        [(HELP, CONTEXT_HELP_STRING1), (ALLOWED_BY_DEFAULT, True)]
    )
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
    context_dict = OrderedDict(
        [
            (HELP, CONTEXT_HELP_STRING1),
            (ALIASES, [CONTEXT3, CONTEXT4]),
            (PARENT, CONTEXT2),
            (ALLOWED_BY_DEFAULT, True),
        ]
    )
    return context, context_dict


@parametrize_with_cases(
    argnames=["context", "expected_context_dict"], cases=THIS_MODULE
)
def test_context_as_dict(context, expected_context_dict):
    context_dict = context.as_dict()
    assert isinstance(context_dict, OrderedDict)
    assert list(context_dict.keys()) == list(expected_context_dict.keys())
    for key, value in expected_context_dict.items():
        assert context_dict[key] == value
