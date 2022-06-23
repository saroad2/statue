import mock

from statue.cli import statue_cli
from statue.command_builder import CommandBuilder
from statue.config.configuration import Configuration
from statue.context import Context
from statue.context_specification import ContextSpecification
from statue.verbosity import DEFAULT_VERBOSITY, VERBOSE
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    COMMAND_HELP_STRING4,
    CONTEXT1,
    CONTEXT2,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    NOT_EXISTING_COMMAND,
)
from tests.util import command_builder_mock, dummy_version, dummy_versions


def test_commands_list(cli_runner, mock_build_configuration_from_file):
    version1, version2 = dummy_versions(2)
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        CommandBuilder(COMMAND1, help=COMMAND_HELP_STRING1),
        CommandBuilder(COMMAND2, help=COMMAND_HELP_STRING2, version=version1),
        CommandBuilder(COMMAND3, help=COMMAND_HELP_STRING3, version=version2),
        CommandBuilder(COMMAND4, help=COMMAND_HELP_STRING4),
    )
    result = cli_runner.invoke(statue_cli, ["commands", "list"])
    assert (
        result.exit_code == 0
    ), f"Exited unsuccessfully with the following exception: {result.exception}"
    assert result.output == (
        f"{COMMAND1} - {COMMAND_HELP_STRING1}\n"
        f"{COMMAND2} (version: {version1}) - {COMMAND_HELP_STRING2}\n"
        f"{COMMAND3} (version: {version2}) - {COMMAND_HELP_STRING3}\n"
        f"{COMMAND4} - {COMMAND_HELP_STRING4}\n"
    ), "List output is different than expected."


def test_commands_show_simple_command(cli_runner, mock_build_configuration_from_file):
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        CommandBuilder(COMMAND2, help=COMMAND_HELP_STRING2, default_args=[ARG3])
    )
    result = cli_runner.invoke(statue_cli, ["commands", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Default arguments - {ARG3}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_version(
    cli_runner, mock_build_configuration_from_file
):
    version = dummy_version()
    configuration = mock_build_configuration_from_file.return_value
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2, help=COMMAND_HELP_STRING2, default_args=[ARG3], version=version
        )
    )
    result = cli_runner.invoke(statue_cli, ["commands", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Version - {version}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Default arguments - {ARG3}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_required_contexts(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2, help=COMMAND_HELP_STRING2, required_contexts=[context1, context2]
        )
    )
    result = cli_runner.invoke(statue_cli, ["commands", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Required contexts - {CONTEXT1}, {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_allowed_contexts(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2, help=COMMAND_HELP_STRING2, allowed_contexts=[context1, context2]
        )
    )
    result = cli_runner.invoke(statue_cli, ["commands", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Allowed contexts - {CONTEXT1}, {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_denied_contexts(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2, help=COMMAND_HELP_STRING2, denied_contexts=[context1, context2]
        )
    )
    result = cli_runner.invoke(statue_cli, ["commands", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Denied contexts - {CONTEXT1}, {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_arguments_override_specified_context(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2,
            help=COMMAND_HELP_STRING2,
            default_args=[ARG1, ARG2],
            contexts_specifications={
                context1: ContextSpecification(args=[ARG3, ARG4]),
            },
        )
    )
    result = cli_runner.invoke(statue_cli, ["commands", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Default arguments - {ARG1} {ARG2}\n"
        "Specified contexts:\n"
        f"\t{CONTEXT1}\n"
        f"\t\tOverride arguments: {ARG3} {ARG4}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_arguments_added_specified_context(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2,
            help=COMMAND_HELP_STRING2,
            default_args=[ARG1, ARG2],
            contexts_specifications={
                context1: ContextSpecification(add_args=[ARG3, ARG4]),
            },
        )
    )
    result = cli_runner.invoke(statue_cli, ["commands", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Default arguments - {ARG1} {ARG2}\n"
        "Specified contexts:\n"
        f"\t{CONTEXT1}\n"
        f"\t\tAdded arguments: {ARG3} {ARG4}\n"
    ), "Show output is different than expected."


def test_commands_show_command_with_clear_arguments_specified_context(
    cli_runner, mock_build_configuration_from_file
):
    configuration = mock_build_configuration_from_file.return_value
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    configuration.commands_repository.add_command_builders(
        CommandBuilder(
            COMMAND2,
            help=COMMAND_HELP_STRING2,
            default_args=[ARG1, ARG2],
            contexts_specifications={
                context1: ContextSpecification(clear_args=True),
            },
        )
    )
    result = cli_runner.invoke(statue_cli, ["commands", "show", COMMAND2])
    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    assert result.output == (
        f"Name - {COMMAND2}\n"
        f"Description - {COMMAND_HELP_STRING2}\n"
        f"Default arguments - {ARG1} {ARG2}\n"
        "Specified contexts:\n"
        f"\t{CONTEXT1}\n"
        "\t\tClears arguments\n"
    ), "Show output is different than expected."


def test_commands_show_unknown_command_side_effect(
    cli_runner, mock_build_configuration_from_file
):
    result = cli_runner.invoke(statue_cli, ["commands", "show", NOT_EXISTING_COMMAND])
    assert result.exit_code == 1, "show command should exit with failure."
    assert (
        result.output == f'Could not find command named "{NOT_EXISTING_COMMAND}"\n'
    ), "Show output is different than expected."


def test_command_install_with_default_verbosity(
    cli_runner, mock_build_configuration_from_file
):
    command_builders = [
        command_builder_mock(name=COMMAND1, installed=False),
        command_builder_mock(name=COMMAND2, installed=False),
        command_builder_mock(name=COMMAND3, installed=False),
    ]
    configuration = Configuration(cache=mock.Mock())
    configuration.commands_repository.add_command_builders(*command_builders)
    mock_build_configuration_from_file.return_value = configuration
    result = cli_runner.invoke(statue_cli, ["commands", "install"])
    for command_builder in command_builders:
        command_builder.install.assert_called_once_with(verbosity=DEFAULT_VERBOSITY)
    assert result.exit_code == 0, "Show command returned with no success code"


def test_command_install_with_verbose(cli_runner, mock_build_configuration_from_file):
    command_builders = [
        command_builder_mock(name=COMMAND1, installed=False),
        command_builder_mock(name=COMMAND2, installed=False),
        command_builder_mock(name=COMMAND3, installed=False),
    ]
    configuration = Configuration(cache=mock.Mock())
    configuration.commands_repository.add_command_builders(*command_builders)
    mock_build_configuration_from_file.return_value = configuration
    result = cli_runner.invoke(statue_cli, ["commands", "install", "--verbose"])
    for command_builder in command_builders:
        command_builder.install.assert_called_with(verbosity=VERBOSE)
    assert result.exit_code == 0, "Show command returned with no success code"


def test_command_install_only_uninstalled(
    cli_runner, mock_build_configuration_from_file
):
    command_builder1, command_builder2, command_builder3 = (
        command_builder_mock(name=COMMAND1, installed=True),
        command_builder_mock(name=COMMAND2, installed=False),
        command_builder_mock(
            name=COMMAND3, installed=True, version="0.2.8", installed_version="0.2.7"
        ),
    )
    configuration = Configuration(cache=mock.Mock())
    configuration.commands_repository.add_command_builders(
        command_builder1, command_builder2, command_builder3
    )
    mock_build_configuration_from_file.return_value = configuration
    result = cli_runner.invoke(statue_cli, ["commands", "install", "--verbose"])
    command_builder1.install.assert_not_called()
    command_builder2.install.assert_called_with(verbosity=VERBOSE)
    command_builder3.install.assert_called_with(verbosity=VERBOSE)
    assert result.exit_code == 0, "Show command returned with no success code"
