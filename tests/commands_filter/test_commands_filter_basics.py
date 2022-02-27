import pytest

from statue.commands_filter import CommandsFilter
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


def test_commands_filter_simple_constructor():
    commands_filter = CommandsFilter()

    assert commands_filter.contexts == frozenset()
    assert commands_filter.allowed_commands is None
    assert commands_filter.denied_commands is None


def test_commands_filter_with_contexts():
    contexts = {
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    }
    commands_filter = CommandsFilter(contexts=contexts)

    assert commands_filter.contexts == contexts
    assert commands_filter.allowed_commands is None
    assert commands_filter.denied_commands is None


def test_commands_filter_with_allowed_commands():
    allowed_commands = {COMMAND1, COMMAND2, COMMAND3}
    commands_filter = CommandsFilter(allowed_commands=allowed_commands)

    assert commands_filter.contexts == frozenset()
    assert commands_filter.allowed_commands == allowed_commands
    assert commands_filter.denied_commands is None


def test_commands_filter_with_denied_commands():
    denied_commands = {COMMAND1, COMMAND2, COMMAND3}
    commands_filter = CommandsFilter(denied_commands=denied_commands)

    assert commands_filter.contexts == frozenset()
    assert commands_filter.allowed_commands is None
    assert commands_filter.denied_commands == denied_commands


def test_commands_filter_repr_string():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    assert str(CommandsFilter(contexts=[context], allowed_commands=[COMMAND1])) == (
        "CommandsFilter("
        f"contexts=frozenset({{{str(context)}}}), "
        f"allowed_commands=frozenset({{'{COMMAND1}'}}), "
        "denied_commands=None)"
    )


def test_commands_filter_contexts_cannot_be_overridden():
    commands_filter = CommandsFilter(
        contexts={
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
            Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        }
    )

    with pytest.raises(AttributeError, match="^can't set attribute$"):
        commands_filter.contexts = {Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)}


def test_commands_filter_allowed_commands_cannot_be_overridden():
    commands_filter = CommandsFilter(allowed_commands={COMMAND1, COMMAND2})

    with pytest.raises(AttributeError, match="^can't set attribute$"):
        commands_filter.allowed_commands = {COMMAND3}


def test_commands_filter_denied_commands_cannot_be_overridden():
    commands_filter = CommandsFilter(denied_commands={COMMAND1, COMMAND2})

    with pytest.raises(AttributeError, match="^can't set attribute$"):
        commands_filter.denied_commands = {COMMAND3}


def test_commands_filter_can_not_have_both_allowed_and_denied_list():

    with pytest.raises(
        ValueError,
        match="^Commands filter cannot be set with both allowed and denied commands$",
    ):
        CommandsFilter(
            allowed_commands={COMMAND1, COMMAND2},
            denied_commands={COMMAND3},
        )
