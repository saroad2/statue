from statue.command_builder import CommandBuilder
from tests.constants import COMMAND1, COMMAND_HELP_STRING1


def test_command_builder_not_installed(mock_get_package):
    mock_get_package.return_value = None
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    assert command_builder.installed_version is None
    assert not command_builder.installed()
    assert command_builder.installed_version_match()
    assert not command_builder.installed_correctly()


def test_command_builder_is_installed_without_specified_version(mock_get_package):
    version = "6.2.1"
    mock_get_package.return_value.version = version
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    assert command_builder.installed_version == version
    assert command_builder.installed()
    assert command_builder.installed_version_match()
    assert command_builder.installed_correctly()


def test_command_builder_is_installed_correctly(mock_get_package):
    version = "6.2.1"
    mock_get_package.return_value.version = version
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )

    assert command_builder.installed_version == version
    assert command_builder.installed()
    assert command_builder.installed_version_match()
    assert command_builder.installed_correctly()


def test_command_builder_is_installed_incorrectly(mock_get_package):
    version, installed_version = "6.2.1", "5.8.1"
    mock_get_package.return_value.version = installed_version
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )

    assert command_builder.installed_version == installed_version
    assert command_builder.installed()
    assert not command_builder.installed_version_match()
    assert not command_builder.installed_correctly()