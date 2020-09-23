from pathlib import Path

import click

from statue.cli import statue as statue_cli

DUMMY_STR = "I'm just a dummy string"


@statue_cli.command("dummy")
def dummy_command():
    """I'm just a dummy command"""
    click.echo(DUMMY_STR)


def test_statue_cli_without_command(cli_runner, empty_configuration):
    result = cli_runner.invoke(statue_cli, [])
    assert result.exit_code == 0, "return code should exit with success."
    assert result.output == (
        "Usage: statue [OPTIONS] COMMAND [ARGS]...\n"
        "\n"
        "  Statue is a static code analysis tools orchestrator.\n"
        "\n"
        "Options:\n"
        "  --version      Show the version and exit.\n"
        "  --config FILE  Statue configuration file.\n"
        "  --help         Show this message and exit.\n"
        "\n"
        "Commands:\n"
        "  command  Commands related actions such as list, install, show, etc.\n"
        "  context  Contexts related actions such as list, show, etc.\n"
        "  dummy    I'm just a dummy command\n"
        "  run      Run static code analysis commands on sources.\n"
    ), "Output is different than expected."


def test_statue_cli_without_config(cli_runner, dummy_cwd, mock_load_configuration):
    result = cli_runner.invoke(statue_cli, ["dummy"])
    assert result.exit_code == 0, "return code should exit with success."
    assert result.output == f"{DUMMY_STR}\n", "Output is different than expected."
    mock_load_configuration.assert_called_with(dummy_cwd / "statue.toml")


def test_statue_cli_with_config(cli_runner, mock_load_configuration, tmpdir):
    config = Path(tmpdir) / "statue.toml"
    config.touch()
    result = cli_runner.invoke(statue_cli, ["--config", str(config), "dummy"])
    assert result.exit_code == 0, "return code should exit with success."
    assert result.output == f"{DUMMY_STR}\n", "Output is different than expected."
    mock_load_configuration.assert_called_with(config)
