from pytest_cases import parametrize

from statue.cli import statue_cli
from statue.exceptions import (
    InconsistentConfiguration,
    InvalidConfiguration,
    MissingConfiguration,
    StatueConfigurationError,
)


@parametrize(argnames="cli_command", argvalues=[["commands", "list"], ["run"]])
@parametrize(
    argnames="config_error",
    argvalues=[
        MissingConfiguration,
        InvalidConfiguration("This is an error message"),
        InconsistentConfiguration("This is an error message"),
        StatueConfigurationError("This is an error message"),
    ],
)
def test_cli_fails_on_missing_configuration(
    cli_runner, cli_command, config_error, mock_build_configuration_from_file
):
    mock_build_configuration_from_file.side_effect = config_error

    result = cli_runner.invoke(statue_cli, cli_command)

    assert result.exit_code == 3
