import pytest
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.commands_filter import CommandsFilter
from statue.context import Context
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
)


def case_empty_filters():
    return CommandsFilter(), CommandsFilter(), CommandsFilter()


def case_merge_contexts_with_nothing():
    filter1 = CommandsFilter(
        contexts={
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
            Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        },
        allowed_commands={COMMAND1, COMMAND2},
    )
    return filter1, CommandsFilter(), filter1


def case_merge_contexts_lists():
    filter1 = CommandsFilter(
        contexts={
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
            Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        },
    )
    filter2 = CommandsFilter(
        contexts={Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)},
    )
    result = CommandsFilter(
        contexts={
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
            Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
            Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        },
    )
    return filter1, filter2, result


def case_merge_allowed_commands_with_nothing():
    filter1 = CommandsFilter(allowed_commands={COMMAND1, COMMAND2, COMMAND3})
    return filter1, CommandsFilter(), filter1


def case_merge_allowed_commands_lists():
    filter1 = CommandsFilter(allowed_commands={COMMAND1, COMMAND2, COMMAND3})
    filter2 = CommandsFilter(allowed_commands={COMMAND1, COMMAND3, COMMAND4})
    result = CommandsFilter(allowed_commands={COMMAND1, COMMAND3})
    return filter1, filter2, result


def case_merge_denied_commands_with_nothing():
    filter1 = CommandsFilter(denied_commands={COMMAND1, COMMAND2, COMMAND3})
    return filter1, CommandsFilter(), filter1


def case_merge_denied_commands_lists():
    filter1 = CommandsFilter(denied_commands={COMMAND1, COMMAND2, COMMAND3})
    filter2 = CommandsFilter(denied_commands={COMMAND1, COMMAND3, COMMAND4})
    result = CommandsFilter(denied_commands=({COMMAND1, COMMAND2, COMMAND3, COMMAND4}))
    return filter1, filter2, result


def case_merge_allowed_and_denied_lists():
    filter1 = CommandsFilter(allowed_commands=({COMMAND1}))
    filter2 = CommandsFilter(denied_commands=({COMMAND2, COMMAND3}))
    result = CommandsFilter(allowed_commands=({COMMAND1}))
    return filter1, filter2, result


@parametrize_with_cases(argnames=["filter1", "filter2", "result"], cases=THIS_MODULE)
def test_commands_filter_merge(
    filter1: CommandsFilter, filter2: CommandsFilter, result: CommandsFilter
):
    assert result == CommandsFilter.merge(filter1, filter2)
    assert result == CommandsFilter.merge(filter2, filter1)


def test_command_filter_merge_fail_on_command_both_allowed_and_denied():
    with pytest.raises(
        ValueError,
        match=(
            "^Cannot merge command filters because the "
            f"following commands are both allowed and denied: {COMMAND1}$"
        ),
    ):
        CommandsFilter.merge(
            CommandsFilter(allowed_commands=([COMMAND1])),
            CommandsFilter(denied_commands=([COMMAND1])),
        )
