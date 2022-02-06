from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli import statue_cli
from statue.constants import ALLOW_LIST, CONTEXTS, DENY_LIST
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    CONTEXT1,
    CONTEXT2,
    SOURCE1,
    SOURCE2,
)
from tests.util import command_mock


def case_no_sources():
    sources_config = {}
    commands_lists = []
    printed_tree = "No sources configuration is specified.\n"
    return sources_config, commands_lists, printed_tree


def case_one_source_empty_configuration():
    sources_config = {SOURCE1: {}}
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} (contexts: empty, allowed: empty, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    return sources_config, commands_lists, printed_tree


def case_one_source_with_configuration():
    sources_config = {
        SOURCE1: {CONTEXTS: [CONTEXT1], ALLOW_LIST: [COMMAND1], DENY_LIST: []}
    }
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} (contexts: {CONTEXT1}, allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    return sources_config, commands_lists, printed_tree


def case_one_source_with_multiple_contexts():
    sources_config = {
        SOURCE1: {CONTEXTS: [CONTEXT1, CONTEXT2], ALLOW_LIST: [COMMAND1], DENY_LIST: []}
    }
    commands_lists = [[command_mock(name=COMMAND1)]]
    printed_tree = (
        f"{SOURCE1} (contexts: {CONTEXT1}, {CONTEXT2}, "
        f"allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
    )
    return sources_config, commands_lists, printed_tree


def case_multiple_sources():
    sources_config = {
        SOURCE1: {
            CONTEXTS: [CONTEXT1, CONTEXT2],
            ALLOW_LIST: [COMMAND1],
            DENY_LIST: [],
        },
        SOURCE2: {CONTEXTS: [], ALLOW_LIST: [COMMAND2, COMMAND3], DENY_LIST: []},
    }
    commands_lists = [
        [command_mock(name=COMMAND1)],
        [command_mock(name=COMMAND2), command_mock(name=COMMAND3)],
    ]
    printed_tree = (
        f"{SOURCE1} (contexts: {CONTEXT1}, {CONTEXT2}, "
        f"allowed: {COMMAND1}, denied: empty):\n"
        f"\t{COMMAND1}\n"
        f"{SOURCE2} (contexts: empty, "
        f"allowed: {COMMAND2}, {COMMAND3}, denied: empty):\n"
        f"\t{COMMAND2}, {COMMAND3}\n"
    )
    return sources_config, commands_lists, printed_tree


@parametrize_with_cases(
    argnames=["sources_config", "commands_lists", "printed_tree"], cases=THIS_MODULE
)
def test_config_show_tree(
    sources_config,
    commands_lists,
    printed_tree,
    cli_runner,
    mock_sources_configuration,
    mock_read_commands,
):
    mock_sources_configuration.return_value = sources_config
    mock_read_commands.side_effect = commands_lists
    result = cli_runner.invoke(statue_cli, ["config", "show-tree"])
    assert (
        result.exit_code == 0
    ), f"Exited with error code. exception: {result.exception}"
    assert result.output == printed_tree
