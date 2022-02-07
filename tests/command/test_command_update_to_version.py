import sys
from unittest import mock

from statue.command import Command
from statue.verbosity import SILENT
from tests.constants import COMMAND1, COMMAND_HELP_STRING1


def test_command_update_to_version(mock_get_package, mock_subprocess, environ):
    mock_get_package.return_value = None
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command.update_to_version()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )


def test_command_will_update_to_version_even_if_already_installed(
    mock_get_package, mock_subprocess, environ
):
    version = "6.2.1"
    mock_get_package.return_value.version = version
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command.update_to_version()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", "-U", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )


def test_command_update_to_version_silently(mock_get_package, mock_subprocess, environ):
    mock_get_package.return_value = None
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    command.update_to_version(verbosity=SILENT)

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", COMMAND1],
        capture_output=True,
        check=False,
        env=environ,
    )


def test_command_update_to_specific_version_when_not_already_installed(
    mock_get_package, mock_subprocess, environ
):
    version = "4.2.1"
    mock_get_package.return_value = None
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, version=version)

    command.update_to_version()

    mock_subprocess.assert_called_once_with(
        [sys.executable, "-m", "pip", "install", f"{COMMAND1}=={version}"],
        capture_output=False,
        check=False,
        env=environ,
    )


def test_command_update_to_specific_version_when_installed_version_match(
    mock_get_package, mock_subprocess, environ
):
    version = "4.2.1"
    mock_get_package.return_value.version = version
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, version=version)

    command.update_to_version()

    mock_subprocess.assert_not_called()


def test_command_update_to_specific_version_when_already_installed(
    mock_subprocess, environ
):
    version, installed_version = "6.2.1", "4.2.1"
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, version=version)

    with mock.patch.object(
        Command, "installed_version", new_callable=mock.PropertyMock
    ) as installed_version_mock:
        installed_version_mock.side_effect = [
            installed_version,
            installed_version,
            installed_version,
            installed_version,
            None,
        ]
        command.update_to_version()

    assert mock_subprocess.call_count == 2
    assert mock_subprocess.call_args_list[0] == mock.call(
        [sys.executable, "-m", "pip", "uninstall", "-y", COMMAND1],
        capture_output=False,
        check=False,
        env=environ,
    )
    assert mock_subprocess.call_args_list[1] == mock.call(
        [sys.executable, "-m", "pip", "install", f"{COMMAND1}=={version}"],
        capture_output=False,
        check=False,
        env=environ,
    )
