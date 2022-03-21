import sys

from statue.command_builder import CommandBuilder
from statue.verbosity import SILENT
from tests.constants import COMMAND1, COMMAND_HELP_STRING1
from tests.util import dummy_version


def test_command_builder_wont_install_if_already_installed(
    mock_get_package, mock_subprocess
):
    version = dummy_version()
    mock_get_package.return_value.version = version
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command_builder.install()

    mock_subprocess.assert_not_called()


def test_command_builder_install_if_not_already_installed(
    mock_get_package, mock_subprocess, environ
):
    mock_get_package.return_value = None
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command_builder.install()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )


def test_command_builder_install_silently(mock_get_package, mock_subprocess, environ):
    mock_get_package.return_value = None
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command_builder.install(verbosity=SILENT)

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", COMMAND1],
        capture_output=True,
        check=False,
        env=environ,
    )


def test_command_builder_install_specified_version(
    mock_get_package, mock_subprocess, environ
):
    version = dummy_version()
    mock_get_package.return_value = None
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )

    command_builder.install()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", f"{COMMAND1}=={version}"],
        capture_output=False,
        check=False,
        env=environ,
    )
