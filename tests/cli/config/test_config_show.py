from statue.cli import statue_cli
from statue.constants import ENCODING


def test_config_show_default_configuration(mock_configuration_path, cli_runner):
    text = """
    This text should be written to file
    It contains multiple lines

    and new lines
    """
    with open(mock_configuration_path.return_value, mode="w", encoding=ENCODING) as fd:
        fd.write(text)
    result = cli_runner.invoke(statue_cli, ["config", "show"])
    assert result.exit_code == 0
    assert result.output == text + "\n"
    mock_configuration_path.assert_called_once_with()


def test_config_show_given_configuration(tmp_path, mock_configuration_path, cli_runner):
    config_path = tmp_path / "statue.toml"
    text = """
    This text should be written to file
    It contains multiple lines

    and new lines
    """
    with open(config_path, mode="w", encoding=ENCODING) as fd:
        fd.write(text)
    result = cli_runner.invoke(
        statue_cli, ["config", "show", "--config", str(config_path)]
    )
    assert result.exit_code == 0
    assert result.output == text + "\n"
    mock_configuration_path.assert_not_called()
