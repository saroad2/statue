import sys

from statue.command_builder import CommandBuilder
from statue.verbosity import SILENT
from tests.constants import COMMAND1, COMMAND_HELP_STRING1


def test_command_builder_update(mock_get_package, mock_subprocess, environ):
    mock_get_package.return_value = None
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command_builder.update()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", "-U", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )


def test_command_builder_will_update_even_if_already_installed(
    mock_get_package, mock_subprocess, environ
):
    version = "6.2.1"
    mock_get_package.return_value.version = version
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command_builder.update()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", "-U", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )


def test_command_builder_update_silently(mock_get_package, mock_subprocess, environ):
    mock_get_package.return_value = None
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command_builder.update(verbosity=SILENT)

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", "-U", COMMAND1],
        capture_output=True,
        check=False,
        env=environ,
    )


def test_command_builder_update_to_latest_even_if_version_is_specified(
    mock_get_package, mock_subprocess, environ
):
    version = "4.2.1"
    mock_get_package.return_value = None
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )

    command_builder.update()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", "-U", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )
