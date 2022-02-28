from typing import List

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.command_builder import CommandBuilder, ContextSpecification
from statue.commands_filter import CommandsFilter
from statue.context import Context
from tests.constants import (
    ARG1,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
)


def case_all_commands_pass():
    commands_filter = CommandsFilter()
    passing_commands = [
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1),
        CommandBuilder(name=COMMAND2, help=COMMAND_HELP_STRING2),
        CommandBuilder(name=COMMAND3, help=COMMAND_HELP_STRING3),
    ]
    non_passing_commands = []

    return commands_filter, passing_commands, non_passing_commands


def case_allowed_commands():
    commands_filter = CommandsFilter(allowed_commands={COMMAND1, COMMAND2})
    passing_commands = [
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1),
        CommandBuilder(name=COMMAND2, help=COMMAND_HELP_STRING2),
    ]
    non_passing_commands = [CommandBuilder(name=COMMAND3, help=COMMAND_HELP_STRING3)]

    return commands_filter, passing_commands, non_passing_commands


def case_denied_commands():
    commands_filter = CommandsFilter(denied_commands={COMMAND1, COMMAND2})
    passing_commands = [CommandBuilder(name=COMMAND3, help=COMMAND_HELP_STRING3)]
    non_passing_commands = [
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1),
        CommandBuilder(name=COMMAND2, help=COMMAND_HELP_STRING2),
    ]

    return commands_filter, passing_commands, non_passing_commands


def case_matching_contexts():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    commands_filter = CommandsFilter(contexts={context1, context2})
    passing_commands = [
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            allowed_contexts=[CONTEXT1, CONTEXT2],
        ),
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            allowed_contexts=[CONTEXT1],
            contexts_specifications={CONTEXT2: ContextSpecification(args=[ARG1])},
        ),
    ]
    non_passing_commands = [
        CommandBuilder(
            name=COMMAND3, help=COMMAND_HELP_STRING3, required_contexts=[CONTEXT3]
        ),
        CommandBuilder(
            name=COMMAND3, help=COMMAND_HELP_STRING3, allowed_contexts=[CONTEXT1]
        ),
    ]

    return commands_filter, passing_commands, non_passing_commands


@parametrize_with_cases(
    argnames=["commands_filter", "passing_commands", "non_passing_commands"],
    cases=THIS_MODULE,
)
def test_commands_filter_pass_filter(
    commands_filter: CommandsFilter,
    passing_commands: List[CommandBuilder],
    non_passing_commands: List[CommandBuilder],
):
    for command_builder in passing_commands:
        assert commands_filter.pass_filter(
            command_builder
        ), f"{command_builder} did not pass filter {commands_filter}"
    for command_builder in non_passing_commands:
        assert not commands_filter.pass_filter(
            command_builder
        ), f"{command_builder} passed filter {commands_filter}"
