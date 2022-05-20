from pathlib import Path

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli import statue_cli
from statue.commands_filter import CommandsFilter
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


def case_no_sources():
    commands_lists = []
    printed_tree = "No sources configuration is specified.\n"
    additional_args = []
    return commands_lists, printed_tree, additional_args


def case_one_source_empty_configuration(mock_build_configuration_from_file):
    configuration = mock_build_configuration_from_file.return_value
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter()
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} (contexts: empty, allowed: empty, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    additional_args = []
    return commands_lists, printed_tree, additional_args


def case_one_source_with_configuration(mock_build_configuration_from_file):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(context)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[context], allowed_commands=[COMMAND1]
    )
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} (contexts: {CONTEXT1}, allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    additional_args = []
    return commands_lists, printed_tree, additional_args


def case_one_source_with_multiple_contexts(mock_build_configuration_from_file):
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(context1, context2)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[context1, context2], allowed_commands=[COMMAND1]
    )
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} (contexts: {CONTEXT1}, {CONTEXT2}, "
        f"allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    additional_args = []
    return commands_lists, printed_tree, additional_args


def case_multiple_sources(mock_build_configuration_from_file):
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(context1, context2)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        contexts=[context1, context2], allowed_commands=[COMMAND1]
    )
    configuration.sources_repository[Path(SOURCE2)] = CommandsFilter(
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
    additional_args = []
    return commands_lists, printed_tree, additional_args


def case_with_context(mock_build_configuration_from_file):
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    )
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        allowed_commands=[COMMAND1]
    )
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} (contexts: {CONTEXT1}, allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    additional_args = ["-c", CONTEXT1]
    return commands_lists, printed_tree, additional_args


def case_with_two_contexts(mock_build_configuration_from_file):
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(
        allowed_commands=[COMMAND1]
    )
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} "
        f"(contexts: {CONTEXT1}, {CONTEXT2}, allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    additional_args = ["-c", CONTEXT1, "-c", CONTEXT2]
    return commands_lists, printed_tree, additional_args


def case_with_allowed_command(mock_build_configuration_from_file):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(context)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(contexts=[context])
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} "
        f"(contexts: {CONTEXT1}, allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    additional_args = ["-a", COMMAND1]
    return commands_lists, printed_tree, additional_args


def case_with_two_allowed_commands(mock_build_configuration_from_file):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(context)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(contexts=[context])
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} "
        f"(contexts: {CONTEXT1}, allowed: {COMMAND1}, {COMMAND2}, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    additional_args = ["-a", COMMAND1, "-a", COMMAND2]
    return commands_lists, printed_tree, additional_args


def case_with_denied_command(mock_build_configuration_from_file):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(context)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(contexts=[context])
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} "
        f"(contexts: {CONTEXT1}, allowed: empty, denied: {COMMAND1}):\n"
        f"\t{COMMAND1}\n"
    )
    additional_args = ["-d", COMMAND1]
    return commands_lists, printed_tree, additional_args


def case_with_two_denied_commands(mock_build_configuration_from_file):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(context)
    configuration.sources_repository[Path(SOURCE1)] = CommandsFilter(contexts=[context])
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} "
        f"(contexts: {CONTEXT1}, allowed: empty, denied: {COMMAND1}, {COMMAND2}):\n"
        f"\t{COMMAND1}\n"
    )
    additional_args = ["-d", COMMAND1, "-d", COMMAND2]
    return commands_lists, printed_tree, additional_args


@parametrize_with_cases(
    argnames=["commands_lists", "printed_tree", "additional_args"], cases=THIS_MODULE
)
def test_config_show_tree(
    commands_lists,
    printed_tree,
    additional_args,
    cli_runner,
    mock_build_configuration_from_file,
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.build_commands.side_effect = commands_lists
    result = cli_runner.invoke(statue_cli, ["show-tree", *additional_args])
    assert (
        result.exit_code == 0
    ), f"Exited with error code. exception: {result.exception}"
    assert result.output == printed_tree
