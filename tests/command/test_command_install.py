import sys

from statue.command import Command
from statue.verbosity import SILENT
from tests.constants import COMMAND1, COMMAND_HELP_STRING1


def test_command_wont_install_if_already_installed(mock_get_package, mock_subprocess):
    version = "6.2.1"
    mock_get_package.return_value.version = version
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command.install()

    mock_subprocess.assert_not_called()


def test_command_install_if_not_already_installed(
    mock_get_package, mock_subprocess, environ
):
    mock_get_package.return_value = None
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command.install()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )


def test_command_install_silently(mock_get_package, mock_subprocess, environ):
    mock_get_package.return_value = None
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command.install(verbosity=SILENT)

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", COMMAND1],
        capture_output=True,
        check=False,
        env=environ,
    )


def test_command_install_specified_version(mock_get_package, mock_subprocess, environ):
    version = "4.2.1"
    mock_get_package.return_value = None
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, version=version)

    command.install()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", f"{COMMAND1}=={version}"],
        capture_output=False,
        check=False,
        env=environ,
    )
