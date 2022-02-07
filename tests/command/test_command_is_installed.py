from statue.command import Command
from tests.constants import COMMAND1, COMMAND_HELP_STRING1


def test_command_not_installed(mock_get_package):
    mock_get_package.return_value = None
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    assert command.installed_version is None
    assert not command.installed()
    assert command.installed_version_match()
    assert not command.installed_correctly()


def test_command_is_installed_without_specified_version(mock_get_package):
    version = "6.2.1"
    mock_get_package.return_value.version = version
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    assert command.installed_version == version
    assert command.installed()
    assert command.installed_version_match()
    assert command.installed_correctly()


def test_command_is_installed_correctly(mock_get_package):
    version = "6.2.1"
    mock_get_package.return_value.version = version
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, version=version)

    assert command.installed_version == version
    assert command.installed()
    assert command.installed_version_match()
    assert command.installed_correctly()


def test_command_is_installed_incorrectly(mock_get_package):
    version, installed_version = "6.2.1", "5.8.1"
    mock_get_package.return_value.version = installed_version
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, version=version)

    assert command.installed_version == installed_version
    assert command.installed()
    assert not command.installed_version_match()
    assert not command.installed_correctly()
