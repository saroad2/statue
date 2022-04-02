from statue.cli import statue_cli
from statue.command_builder import CommandBuilder, ContextSpecification
from statue.context import Context
from tests.constants import (
    ARG1,
    ARG2,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
    COMMAND6,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    COMMAND_HELP_STRING4,
    COMMAND_HELP_STRING5,
    COMMAND_HELP_STRING6,
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
    NOT_EXISTING_CONTEXT,
)


def test_contexts_list_of_full_configuration(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
    )
    result = cli_runner.invoke(statue_cli, ["context", "list"])
    assert result.exit_code == 0, "list contexts should exit with success."
    assert result.output == (
        f"{CONTEXT1} - {CONTEXT_HELP_STRING1}\n"
        f"{CONTEXT2} - {CONTEXT_HELP_STRING2}\n"
        f"{CONTEXT3} - {CONTEXT_HELP_STRING3}\n"
        f"{CONTEXT4} - {CONTEXT_HELP_STRING4}\n"
        f"{CONTEXT5} - {CONTEXT_HELP_STRING5}\n"
    ), "List output is different than expected."


def test_contexts_list_of_an_empty_configuration(
    cli_runner, mock_build_configuration_from_file
):
    result = cli_runner.invoke(statue_cli, ["context", "list"])
    assert result.exit_code == 1, "list contexts should exit with failure."
    assert (
        result.output == "No contexts were found.\n"
    ), "List output is different than expected."


def test_contexts_show_simple_context(cli_runner, mock_build_configuration_from_file):
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
    )
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT2])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT2}\n" f"Description - {CONTEXT_HELP_STRING2}\n"
    ), "Show output is different than expected."


def test_contexts_show_context_with_one_alias(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    )
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Aliases - {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_contexts_show_context_with_two_aliases(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3])
    )
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Aliases - {CONTEXT2}, {CONTEXT3}\n"
    ), "Show output is different than expected."


def test_contexts_show_context_with_parent(
    cli_runner, mock_build_configuration_from_file
):
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(context, parent)
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Parent - {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_contexts_show_context_required_by_command(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[context]
        )
    )
    configuration.contexts_repository.add_contexts(context)
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Required by - {COMMAND1}\n"
    ), "Show output is different than expected."


def test_contexts_show_context_allowed_for_command(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[context]
        )
    )
    configuration.contexts_repository.add_contexts(context)
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Allowed for - {COMMAND1}\n"
    ), "Show output is different than expected."


def test_contexts_show_context_specified_for_command(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            contexts_specifications={context: ContextSpecification(args=[ARG1])},
        )
    )
    configuration.contexts_repository.add_contexts(context)
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Specified for - {COMMAND1}\n"
    ), "Show output is different than expected."


def test_contexts_show_context_with_multiple_available_commands(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[context]
        ),
        CommandBuilder(
            name=COMMAND2, help=COMMAND_HELP_STRING2, required_contexts=[context]
        ),
        CommandBuilder(
            name=COMMAND3, help=COMMAND_HELP_STRING3, allowed_contexts=[context]
        ),
        CommandBuilder(
            name=COMMAND4, help=COMMAND_HELP_STRING4, allowed_contexts=[context]
        ),
        CommandBuilder(
            name=COMMAND5,
            help=COMMAND_HELP_STRING5,
            contexts_specifications={context: ContextSpecification(args=[ARG1])},
        ),
        CommandBuilder(
            name=COMMAND6,
            help=COMMAND_HELP_STRING6,
            contexts_specifications={context: ContextSpecification(args=[ARG2])},
        ),
    )
    configuration.contexts_repository.add_contexts(context)
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Required by - {COMMAND1}, {COMMAND2}\n"
        f"Allowed for - {COMMAND3}, {COMMAND4}\n"
        f"Specified for - {COMMAND5}, {COMMAND6}\n"
    ), "Show output is different than expected."


def test_contexts_show_non_existing_context(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
    )
    result = cli_runner.invoke(statue_cli, ["context", "show", NOT_EXISTING_CONTEXT])
    assert result.exit_code == 1, "show context should exit with failure."
    assert (
        result.output == f'Could not find the context "{NOT_EXISTING_CONTEXT}".\n'
    ), "Show output is different than expected."
