import random
from unittest import mock

import pytest

from statue.command import Command, CommandEvaluation
from statue.exceptions import CommandExecutionError
from tests.constants import COMMAND1, COMMAND_HELP_STRING1, SOURCE1


def mock_subprocess_response(exit_code, stdout, stderr):
    subprocess_response = mock.Mock()
    subprocess_response.returncode = exit_code
    subprocess_response.stdout.decode.return_value = stdout
    subprocess_response.stderr.decode.return_value = stderr
    return subprocess_response


def test_simple_command_execute(mock_subprocess, environ):
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    subprocess_response = mock_subprocess_response(exit_code=0, stdout="", stderr="")
    mock_subprocess.return_value = subprocess_response

    command_evaluation = command.execute(source)

    assert command_evaluation == CommandEvaluation(
        command=command, success=True, captured_output=[]
    )
    mock_subprocess.assert_called_once_with(
        [COMMAND1, SOURCE1], capture_output=True, check=False, env=environ
    )
    subprocess_response.stdout.decode.assert_called_once_with("utf-8")
    subprocess_response.stderr.decode.assert_called_once_with("utf-8")


def test_command_execute_with_args(mock_subprocess, environ):
    args = ["a", "b", "c", "d"]
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=args)
    subprocess_response = mock_subprocess_response(exit_code=0, stdout="", stderr="")
    mock_subprocess.return_value = subprocess_response

    command_evaluation = command.execute(source)

    assert command_evaluation == CommandEvaluation(
        command=command, success=True, captured_output=[]
    )
    mock_subprocess.assert_called_once_with(
        [COMMAND1, SOURCE1, *args], capture_output=True, check=False, env=environ
    )
    subprocess_response.stdout.decode.assert_called_once_with("utf-8")
    subprocess_response.stderr.decode.assert_called_once_with("utf-8")


def test_command_execute_with_non_zero_exit_code(mock_subprocess, environ):
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    subprocess_response = mock_subprocess_response(
        exit_code=random.randint(1, 10), stdout="", stderr=""
    )
    mock_subprocess.return_value = subprocess_response

    command_evaluation = command.execute(source)

    assert command_evaluation == CommandEvaluation(
        command=command, success=False, captured_output=[]
    )
    mock_subprocess.assert_called_once_with(
        [COMMAND1, SOURCE1], capture_output=True, check=False, env=environ
    )
    subprocess_response.stdout.decode.assert_called_once_with("utf-8")
    subprocess_response.stderr.decode.assert_called_once_with("utf-8")


def test_command_execute_with_one_line_stdout(mock_subprocess, environ):
    stdout_line = "This is a line"
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    subprocess_response = mock_subprocess_response(
        exit_code=0, stdout=stdout_line, stderr=""
    )
    mock_subprocess.return_value = subprocess_response

    command_evaluation = command.execute(source)

    assert command_evaluation == CommandEvaluation(
        command=command, success=True, captured_output=[stdout_line]
    )
    mock_subprocess.assert_called_once_with(
        [COMMAND1, SOURCE1], capture_output=True, check=False, env=environ
    )
    subprocess_response.stdout.decode.assert_called_once_with("utf-8")
    subprocess_response.stderr.decode.assert_called_once_with("utf-8")


def test_command_execute_with_two_lines_stdout(mock_subprocess, environ):
    stdout = ["This is a line", "This is also a line"]
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    subprocess_response = mock_subprocess_response(
        exit_code=0, stdout="\n".join(stdout), stderr=""
    )
    mock_subprocess.return_value = subprocess_response

    command_evaluation = command.execute(source)

    assert command_evaluation == CommandEvaluation(
        command=command, success=True, captured_output=stdout
    )
    mock_subprocess.assert_called_once_with(
        [COMMAND1, SOURCE1], capture_output=True, check=False, env=environ
    )
    subprocess_response.stdout.decode.assert_called_once_with("utf-8")
    subprocess_response.stderr.decode.assert_called_once_with("utf-8")


def test_command_execute_with_one_line_stderr(mock_subprocess, environ):
    stderr_line = "This is a line"
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    subprocess_response = mock_subprocess_response(
        exit_code=0, stdout="", stderr=stderr_line
    )
    mock_subprocess.return_value = subprocess_response

    command_evaluation = command.execute(source)

    assert command_evaluation == CommandEvaluation(
        command=command, success=True, captured_output=[stderr_line]
    )
    mock_subprocess.assert_called_once_with(
        [COMMAND1, SOURCE1], capture_output=True, check=False, env=environ
    )
    subprocess_response.stdout.decode.assert_called_once_with("utf-8")
    subprocess_response.stderr.decode.assert_called_once_with("utf-8")


def test_command_execute_with_two_lines_stderr(mock_subprocess, environ):
    stderr = ["This is a line", "This is also a line"]
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    subprocess_response = mock_subprocess_response(
        exit_code=0, stdout="", stderr="\n".join(stderr)
    )
    mock_subprocess.return_value = subprocess_response

    command_evaluation = command.execute(source)

    assert command_evaluation == CommandEvaluation(
        command=command, success=True, captured_output=stderr
    )
    mock_subprocess.assert_called_once_with(
        [COMMAND1, SOURCE1], capture_output=True, check=False, env=environ
    )
    subprocess_response.stdout.decode.assert_called_once_with("utf-8")
    subprocess_response.stderr.decode.assert_called_once_with("utf-8")


def test_command_execute_with_both_stdout_and_stderr(mock_subprocess, environ):
    stdout_line, stderr_line = "This is an stdout line", "This is an stderr line"
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    subprocess_response = mock_subprocess_response(
        exit_code=0, stdout=stdout_line, stderr=stderr_line
    )
    mock_subprocess.return_value = subprocess_response

    command_evaluation = command.execute(source)

    assert command_evaluation == CommandEvaluation(
        command=command, success=True, captured_output=[stderr_line]
    )
    mock_subprocess.assert_called_once_with(
        [COMMAND1, SOURCE1], capture_output=True, check=False, env=environ
    )
    subprocess_response.stdout.decode.assert_called_once_with("utf-8")
    subprocess_response.stderr.decode.assert_called_once_with("utf-8")


def test_command_execute_raises_file_not_found_exception(mock_subprocess):
    mock_subprocess.side_effect = FileNotFoundError
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    source = SOURCE1
    with pytest.raises(
        CommandExecutionError,
        match=f'^Cannot execute "{COMMAND1}" because it is not installed.$',
    ):
        command.execute(source)
