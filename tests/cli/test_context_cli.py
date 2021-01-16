from statue.cli import statue as statue_cli
from statue.command import Command
from statue.constants import STANDARD
from statue.context import Context
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT5,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
    CONTEXT_HELP_STRING4,
    CONTEXT_HELP_STRING5,
    CONTEXTS_MAP,
    NOT_EXISTING_CONTEXT,
    STANDARD_HELP,
)
from tests.util import build_contexts_map


def test_contexts_list_of_full_configuration(
    cli_runner, empty_configuration, mock_contexts_map
):
    mock_contexts_map.return_value = CONTEXTS_MAP
    result = cli_runner.invoke(statue_cli, ["context", "list"])
    assert result.exit_code == 0, "list contexts should exit with success."
    assert result.output == (
        f"{STANDARD} - {STANDARD_HELP}\n"
        f"{CONTEXT1} - {CONTEXT_HELP_STRING1}\n"
        f"{CONTEXT2} - {CONTEXT_HELP_STRING2}\n"
        f"{CONTEXT3} - {CONTEXT_HELP_STRING3}\n"
        f"{CONTEXT4} - {CONTEXT_HELP_STRING4}\n"
        f"{CONTEXT5} - {CONTEXT_HELP_STRING5}\n"
    ), "List output is different than expected."


def test_contexts_list_of_an_empty_configuration(
    cli_runner, empty_configuration, mock_contexts_map
):
    mock_contexts_map.return_value = None
    result = cli_runner.invoke(statue_cli, ["context", "list"])
    assert result.exit_code == 1, "list contexts should exit with failure."
    assert (
        result.output == "No contexts were found.\n"
    ), "List output is different than expected."


def test_contexts_show_of_context(
    cli_runner, empty_configuration, mock_contexts_map, mock_read_commands
):
    mock_contexts_map.return_value = CONTEXTS_MAP
    mock_read_commands.return_value = [
        Command(COMMAND1, help=COMMAND_HELP_STRING1),
        Command(COMMAND2, help=COMMAND_HELP_STRING2),
    ]
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT2])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT2}\n"
        f"Description - {CONTEXT_HELP_STRING2}\n"
        f"Matching commands - {COMMAND1}, {COMMAND2}\n"
    ), "Show output is different than expected."
    mock_read_commands.assert_called_once_with(contexts=[CONTEXT2])


def test_contexts_show_of_context_with_one_alias(
    cli_runner, empty_configuration, mock_contexts_map, mock_read_commands
):
    mock_contexts_map.return_value = build_contexts_map(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    )
    mock_read_commands.return_value = [
        Command(COMMAND1, help=COMMAND_HELP_STRING1),
        Command(COMMAND2, help=COMMAND_HELP_STRING2),
    ]
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Aliases - {CONTEXT2}\n"
        f"Matching commands - {COMMAND1}, {COMMAND2}\n"
    ), "Show output is different than expected."
    mock_read_commands.assert_called_once_with(contexts=[CONTEXT1])


def test_contexts_show_of_context_with_two_aliases(
    cli_runner, empty_configuration, mock_contexts_map, mock_read_commands
):
    mock_contexts_map.return_value = build_contexts_map(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3])
    )
    mock_read_commands.return_value = [
        Command(COMMAND1, help=COMMAND_HELP_STRING1),
        Command(COMMAND2, help=COMMAND_HELP_STRING2),
    ]
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Aliases - {CONTEXT2}, {CONTEXT3}\n"
        f"Matching commands - {COMMAND1}, {COMMAND2}\n"
    ), "Show output is different than expected."
    mock_read_commands.assert_called_once_with(contexts=[CONTEXT1])


def test_contexts_show_of_context_with_parent(
    cli_runner, empty_configuration, mock_contexts_map, mock_read_commands
):
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    mock_contexts_map.return_value = build_contexts_map(context, parent)
    mock_read_commands.return_value = [Command(COMMAND1, help=COMMAND_HELP_STRING1)]
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Parent - {CONTEXT2}\n"
        f"Matching commands - {COMMAND1}\n"
    ), "Show output is different than expected."
    mock_read_commands.assert_called_once_with(contexts=[CONTEXT1])


def test_contexts_show_of_non_existing_context(
    cli_runner, empty_configuration, mock_contexts_map
):
    mock_contexts_map.return_value = CONTEXTS_MAP
    result = cli_runner.invoke(statue_cli, ["context", "show", NOT_EXISTING_CONTEXT])
    assert result.exit_code == 1, "show context should exit with failure."
    assert (
        result.output == f'Could not find the context "{NOT_EXISTING_CONTEXT}".\n'
    ), "Show output is different than expected."
