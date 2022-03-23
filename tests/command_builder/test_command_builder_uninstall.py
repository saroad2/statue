import sys

from statue.command_builder import CommandBuilder
from statue.verbosity import SILENT
from tests.constants import COMMAND1, COMMAND_HELP_STRING1
from tests.util import dummy_version


def test_command_builder_uninstall(mock_get_package, mock_subprocess, environ):
    version = dummy_version()
    mock_get_package.return_value.version = version
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command_builder.uninstall()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "uninstall", "-y", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )


def test_command_builder_uninstall_if_not_already_uninstalled(
    mock_get_package, mock_subprocess
):
    mock_get_package.return_value = None
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command_builder.uninstall()

    mock_subprocess.assert_not_called()


def test_command_builder_uninstall_silently(mock_get_package, mock_subprocess, environ):
    version = dummy_version()
    mock_get_package.return_value.version = version
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command_builder.uninstall(verbosity=SILENT)

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "uninstall", "-y", COMMAND1],
        capture_output=True,
        check=False,
        env=environ,
    )


def test_command_builder_uninstall_specified_version(
    mock_get_package, mock_subprocess, environ
):
    version, installed_version = dummy_version(), dummy_version()
    mock_get_package.return_value.version = installed_version
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )

    command_builder.uninstall()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "uninstall", "-y", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )
