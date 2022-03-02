from pytest_cases import parametrize

from statue.cli import statue_cli
from statue.exceptions import MissingConfiguration


@parametrize(argnames="cli_command", argvalues=[["command", "list"], ["run"]])
def test_cli_fails_on_missing_configuration(
    cli_runner, cli_command, mock_build_configuration_from_file
):
    mock_build_configuration_from_file.side_effect = MissingConfiguration

    result = cli_runner.invoke(statue_cli, cli_command)

    assert result.exit_code == 3
    assert result.output == "Statue was unable to load configuration\n"
