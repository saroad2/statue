from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.commands_filter import CommandsFilter
from statue.constants import ALLOW_LIST, CONTEXTS, DENY_LIST
from statue.context import Context
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
)


def case_empty_commands_filter():
    commands_filter = CommandsFilter()
    filter_dict = {}
    return commands_filter, filter_dict


def case_commands_filter_with_contexts():
    commands_filter = CommandsFilter(
        contexts=[
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
            Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
            Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        ]
    )
    filter_dict = {CONTEXTS: [CONTEXT1, CONTEXT2, CONTEXT3]}
    return commands_filter, filter_dict


def case_commands_filter_with_allowed_commands():
    commands_filter = CommandsFilter(allowed_commands=[COMMAND1, COMMAND2, COMMAND3])
    filter_dict = {ALLOW_LIST: [COMMAND1, COMMAND2, COMMAND3]}
    return commands_filter, filter_dict


def case_commands_filter_with_denied_commands():
    commands_filter = CommandsFilter(denied_commands=[COMMAND1, COMMAND2, COMMAND3])
    filter_dict = {DENY_LIST: [COMMAND1, COMMAND2, COMMAND3]}
    return commands_filter, filter_dict


@parametrize_with_cases(argnames=["commands_filter", "filter_dict"], cases=THIS_MODULE)
def test_commands_filter_as_dict(commands_filter, filter_dict):
    assert commands_filter.as_dict() == filter_dict
