import sys
from argparse import Namespace

import pytest
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.command import Command
from statue.exceptions import CommandExecutionError
from statue.verbosity import SILENT, VERBOSE
from tests.constants import (
    ARG1,
    ARG2,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    SOURCE1, VERSION1,
)

COMMANDS = [COMMAND1, COMMAND2, COMMAND3]


def packages(commands_list):
    return [Namespace(key=command) for command in commands_list]


def case_no_args():
    inp = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    output = dict(
        name=COMMAND1,
        install_name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        args=[],
        command_input=[COMMAND1, SOURCE1],
        print=f'Running the following command: "{COMMAND1} {SOURCE1}"',
        repr=f"Command(name='{COMMAND1}', help='{COMMAND_HELP_STRING1}', args=[], version=None)",
    )
    return inp, output


def case_one_arg():
    inp = Command(name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG1])
    output = dict(
        name=COMMAND2,
        install_name=COMMAND2,
        help=COMMAND_HELP_STRING2,
        args=[ARG1],
        command_input=[COMMAND2, SOURCE1, ARG1],
        print=f'Running the following command: "{COMMAND2} {SOURCE1} {ARG1}"',
        repr=(
            f"Command(name='{COMMAND2}', help='{COMMAND_HELP_STRING2}', "
            f"args=['{ARG1}'], version=None)"
        ),
    )
    return inp, output


def case_two_args():
    inp = Command(name=COMMAND3, help=COMMAND_HELP_STRING3, args=[ARG1, ARG2])
    output = dict(
        name=COMMAND3,
        install_name=COMMAND3,
        help=COMMAND_HELP_STRING3,
        args=[ARG1, ARG2],
        command_input=[COMMAND3, SOURCE1, ARG1, ARG2],
        print=(
            "Running the following command: " f'"{COMMAND3} {SOURCE1} {ARG1} {ARG2}"'
        ),
        repr=(
            f"Command(name='{COMMAND3}', help='{COMMAND_HELP_STRING3}',"
            f" args=['{ARG1}', '{ARG2}'], version=None)"
        ),
    )
    return inp, output


def case_specified_version():
    inp = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, version=VERSION1)
    output = dict(
        name=COMMAND1,
        install_name=f"{COMMAND1}=={VERSION1}",
        help=COMMAND_HELP_STRING1,
        args=[],
        command_input=[COMMAND1, SOURCE1],
        print=f'Running the following command: "{COMMAND1} {SOURCE1}"',
        repr=f"Command(name='{COMMAND1}', help='{COMMAND_HELP_STRING1}', args=[], version='{VERSION1}')",
    )
    return inp, output


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_name_is_set(command, out):
    assert command.name == out["name"]


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_help_is_set(command, out):
    assert command.help == out["help"]


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_args_are_set(command, out):
    assert command.args == out["args"]


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_execute(command, out, mock_subprocess, environ):
    command.execute(SOURCE1)
    mock_subprocess.assert_called_with(
        out["command_input"], env=environ, check=False, capture_output=False
    )


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_execute_raises_error(command, out, mock_subprocess, environ):
    mock_subprocess.side_effect = FileNotFoundError()
    with pytest.raises(
        CommandExecutionError,
        match=f'^Cannot execute "{command.name}" because it is not installed.$',
    ):
        command.execute(SOURCE1)


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_execute_silently(command, out, mock_subprocess, environ):
    command.execute(SOURCE1, verbosity=SILENT)
    mock_subprocess.assert_called_with(
        out["command_input"], env=environ, check=False, capture_output=True
    )


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_execute_verbosely(command, out, mock_subprocess, environ, print_mock):
    command.execute(SOURCE1, verbosity=VERBOSE)
    mock_subprocess.assert_called_with(
        out["command_input"], env=environ, check=False, capture_output=False
    )
    print_mock.assert_called_with(out["print"])


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_representation_string(command, out):
    assert str(command) == out["repr"]


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_installed_returns_true(command, out, mock_get_package):
    assert command.installed(), "Command where supposed to be installed, but it wasn't"


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_installed_returns_false(command, out, mock_get_package):
    mock_get_package.return_value = None
    assert (
        not command.installed()
    ), "Command where supposed not to be installed, but it was"


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_install_command_with_normal_verbosity(
    command, out, mock_subprocess, environ, print_mock
):
    command.install()
    install_name = out['install_name']
    mock_subprocess.assert_called_with(
        [sys.executable, "-m", "pip", "install", install_name],
        env=environ,
        check=False,
        capture_output=False,
    )
    print_mock.assert_called_with(f"Installing {install_name}")


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_install_command_silently(command, out, mock_subprocess, environ, print_mock):
    command.install(verbosity=SILENT)
    install_name = out["install_name"]
    mock_subprocess.assert_called_with(
        [sys.executable, "-m", "pip", "install", install_name],
        env=environ,
        check=False,
        capture_output=True,
    )
    print_mock.assert_not_called()


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_install_when_already_installed(
    command, out, mock_subprocess, mock_get_package
):
    command.install()
    mock_subprocess.assert_not_called()


def test_command_equals():
    name = "command1"
    help_string = "help1"
    args = ["arg1", "arg2", "arg3"]
    command1 = Command(name=name, help=help_string, args=args)
    command2 = Command(name=name, help=help_string, args=args)
    assert command1 == command2
    assert not command1 != command2  # pylint: disable=C0113


def test_command_not_equals_because_of_different_names():
    name1 = "command1"
    name2 = "command2"
    help_string = "help1"
    args = ["arg1", "arg2", "arg3"]
    command1 = Command(name=name1, help=help_string, args=args)
    command2 = Command(name=name2, help=help_string, args=args)
    assert not command1 == command2  # pylint: disable=C0113
    assert command1 != command2


def test_command_not_equals_because_of_different_helps():
    name = "command1"
    help_string1 = "help1"
    help_string2 = "help2"
    args = ["arg1", "arg2", "arg3"]
    command1 = Command(name=name, help=help_string1, args=args)
    command2 = Command(name=name, help=help_string2, args=args)
    assert not command1 == command2  # pylint: disable=C0113
    assert command1 != command2


def test_command_not_equals_because_of_different_args():
    name = "command1"
    help_string = "help1"
    args1 = ["arg1", "arg2", "arg3"]
    args2 = ["arg4", "arg5"]
    command1 = Command(name=name, help=help_string, args=args1)
    command2 = Command(name=name, help=help_string, args=args2)
    assert not command1 == command2  # pylint: disable=C0113
    assert command1 != command2
