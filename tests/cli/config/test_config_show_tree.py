from pathlib import Path

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli import statue_cli
from statue.commands_filter import CommandsFilter
from statue.configuration import Configuration
from statue.context import Context
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    CONTEXT1,
    CONTEXT2,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    SOURCE1,
    SOURCE2,
)
from tests.util import command_mock


def case_no_sources(clear_configuration):
    commands_lists = []
    printed_tree = "No sources configuration is specified.\n"
    return commands_lists, printed_tree


def case_one_source_empty_configuration(clear_configuration):
    Configuration.sources_repository[Path(SOURCE1)] = CommandsFilter()
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} (contexts: empty, allowed: empty, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    return commands_lists, printed_tree


def case_one_source_with_configuration(clear_configuration):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    Configuration.contexts_repository.add_contexts(context)
    Configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[context], allowed_commands=[COMMAND1]
    )
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} (contexts: {CONTEXT1}, allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    return commands_lists, printed_tree


def case_one_source_with_multiple_contexts(clear_configuration):
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    Configuration.contexts_repository.add_contexts(context1, context2)
    Configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[context1, context2], allowed_commands=[COMMAND1]
    )
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} (contexts: {CONTEXT1}, {CONTEXT2}, "
        f"allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    return commands_lists, printed_tree


def case_multiple_sources(clear_configuration):
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    Configuration.contexts_repository.add_contexts(context1, context2)
    Configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[context1, context2], allowed_commands=[COMMAND1]
    )
    Configuration.sources_repository[Path(SOURCE2)] = CommandsFilter(
        denied_commands=[COMMAND2, COMMAND3]
    )
    commands_lists = [
        [command_mock(name=COMMAND1)],
        [command_mock(name=COMMAND2), command_mock(name=COMMAND3)],
    ]
    printed_tree = (
        f"{SOURCE1} (contexts: {CONTEXT1}, {CONTEXT2}, "
        f"allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
        f"{SOURCE2} (contexts: empty, "
        f"allowed: empty, denied: {COMMAND2}, {COMMAND3}):\n"
        f"\t{COMMAND2}, {COMMAND3}\n"
    )
    return commands_lists, printed_tree


@parametrize_with_cases(argnames=["commands_lists", "printed_tree"], cases=THIS_MODULE)
def test_config_show_tree(
    commands_lists,
    printed_tree,
    cli_runner,
    mock_build_commands,
    mock_load_configuration,
):
    mock_build_commands.side_effect = commands_lists
    result = cli_runner.invoke(statue_cli, ["config", "show-tree"])
    assert (
        result.exit_code == 0
    ), f"Exited with error code. exception: {result.exception}"
    assert result.output == printed_tree
