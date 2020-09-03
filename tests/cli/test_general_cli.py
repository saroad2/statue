from statue.cli import statue as statue_cli


def test_statue_cli_without_command(cli_runner, full_configuration):
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
        "  run      Run static code analysis commands on sources.\n"
    ), "output is different than expected."
