import sys

from statue.command import Command
from statue.verbosity import SILENT
from tests.constants import COMMAND1, COMMAND_HELP_STRING1


def test_command_uninstall(mock_get_package, mock_subprocess, environ):
    version = "6.2.1"
    mock_get_package.return_value.version = version
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command.uninstall()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "uninstall", "-y", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )


def test_command_uninstall_if_not_already_uninstalled(
    mock_get_package, mock_subprocess
):
    mock_get_package.return_value = None
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command.uninstall()

    mock_subprocess.assert_not_called()


def test_command_uninstall_silently(mock_get_package, mock_subprocess, environ):
    version = "6.2.1"
    mock_get_package.return_value.version = version
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command.uninstall(verbosity=SILENT)

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "uninstall", "-y", COMMAND1],
        capture_output=True,
        check=False,
        env=environ,
    )


def test_command_uninstall_specified_version(
    mock_get_package, mock_subprocess, environ
):
    version, installed_version = "4.2.1", "6.2.1"
    mock_get_package.return_value.version = installed_version
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, version=version)

    command.uninstall()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "uninstall", "-y", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )
