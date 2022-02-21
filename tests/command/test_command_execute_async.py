import asyncio
import random

import mock
import pytest
import pytest_asyncio

from statue.command import Command, CommandEvaluation
from statue.exceptions import CommandExecutionError
from statue.sources_locks_repository import SourcesLocksRepository
from tests.constants import COMMAND1, COMMAND_HELP_STRING1, SOURCE1
from tests.util import assert_equal_command_evaluations, set_execution_duration


@pytest_asyncio.fixture
async def mock_get_source_lock():
    with mock.patch.object(
        SourcesLocksRepository, "get_lock", new_callable=mock.AsyncMock
    ) as get_lock_mock:
        get_lock_mock.return_value = mock.Mock()
        get_lock_mock.return_value.acquire = mock.AsyncMock()
        get_lock_mock.return_value.release = mock.Mock()
        yield get_lock_mock


@pytest_asyncio.fixture
async def mock_async_create_subprocess():
    with mock.patch.object(
        asyncio, "create_subprocess_exec", new_callable=mock.AsyncMock
    ) as create_subprocess_exec_mock:
        yield create_subprocess_exec_mock


def set_async_subprocess_response(mock_async_subprocess, exit_code, stdout, stderr):
    mock_async_subprocess.return_value.returncode = exit_code
    stdout_mock, stderr_mock = mock.Mock(), mock.Mock()
    mock_async_subprocess.return_value.communicate = mock.AsyncMock(
        return_value=(stdout_mock, stderr_mock)
    )
    stdout_mock.decode.return_value = stdout
    stderr_mock.decode.return_value = stderr


@pytest.mark.asyncio
async def test_simple_command_execute(
    mock_async_create_subprocess, mock_get_source_lock, environ, mock_time
):
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    set_async_subprocess_response(
        mock_async_create_subprocess, exit_code=0, stdout="", stderr=""
    )

    execution_duration = set_execution_duration(mock_time)

    command_evaluation = await command.execute_async(source)

    mock_get_source_lock.assert_awaited_once_with(SOURCE1)
    mock_get_source_lock.return_value.acquire.assert_awaited_once_with()
    mock_get_source_lock.return_value.release.assert_called_once_with()
    assert_equal_command_evaluations(
        command_evaluation,
        CommandEvaluation(
            command=command,
            success=True,
            captured_output=[],
            execution_duration=execution_duration,
        ),
    )
    mock_async_create_subprocess.assert_called_once_with(
        COMMAND1,
        SOURCE1,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=environ,
    )
    (
        stdout_mock,
        stderr_mock,
    ) = mock_async_create_subprocess.return_value.communicate.return_value
    stdout_mock.decode.assert_called_once_with("utf-8")
    stderr_mock.decode.assert_called_once_with("utf-8")


@pytest.mark.asyncio
async def test_command_execute_with_args(
    mock_async_create_subprocess, mock_get_source_lock, environ, mock_time
):
    args = ["a", "b", "c", "d"]
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=args)
    set_async_subprocess_response(
        mock_async_create_subprocess, exit_code=0, stdout="", stderr=""
    )

    execution_duration = set_execution_duration(mock_time)

    command_evaluation = await command.execute_async(source)

    mock_get_source_lock.assert_awaited_once_with(SOURCE1)
    mock_get_source_lock.return_value.acquire.assert_awaited_once_with()
    mock_get_source_lock.return_value.release.assert_called_once_with()
    assert_equal_command_evaluations(
        command_evaluation,
        CommandEvaluation(
            command=command,
            execution_duration=execution_duration,
            success=True,
            captured_output=[],
        ),
    )
    mock_async_create_subprocess.assert_called_once_with(
        COMMAND1,
        SOURCE1,
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=environ,
    )
    (
        stdout_mock,
        stderr_mock,
    ) = mock_async_create_subprocess.return_value.communicate.return_value
    stdout_mock.decode.assert_called_once_with("utf-8")
    stderr_mock.decode.assert_called_once_with("utf-8")


@pytest.mark.asyncio
async def test_command_execute_with_non_zero_exit_code(
    mock_async_create_subprocess, mock_get_source_lock, environ, mock_time
):
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    set_async_subprocess_response(
        mock_async_create_subprocess,
        exit_code=random.randint(1, 10),
        stdout="",
        stderr="",
    )

    execution_duration = set_execution_duration(mock_time)

    command_evaluation = await command.execute_async(source)

    mock_get_source_lock.assert_awaited_once_with(SOURCE1)
    mock_get_source_lock.return_value.acquire.assert_awaited_once_with()
    mock_get_source_lock.return_value.release.assert_called_once_with()
    assert_equal_command_evaluations(
        command_evaluation,
        CommandEvaluation(
            command=command,
            execution_duration=execution_duration,
            success=False,
            captured_output=[],
        ),
    )
    mock_async_create_subprocess.assert_called_once_with(
        COMMAND1,
        SOURCE1,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=environ,
    )
    (
        stdout_mock,
        stderr_mock,
    ) = mock_async_create_subprocess.return_value.communicate.return_value
    stdout_mock.decode.assert_called_once_with("utf-8")
    stderr_mock.decode.assert_called_once_with("utf-8")


@pytest.mark.asyncio
async def test_command_execute_with_one_line_stdout(
    mock_async_create_subprocess, mock_get_source_lock, environ, mock_time
):
    stdout_line = "This is a line"
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    set_async_subprocess_response(
        mock_async_create_subprocess, exit_code=0, stdout=stdout_line, stderr=""
    )

    execution_duration = set_execution_duration(mock_time)

    command_evaluation = await command.execute_async(source)

    mock_get_source_lock.assert_awaited_once_with(SOURCE1)
    mock_get_source_lock.return_value.acquire.assert_awaited_once_with()
    mock_get_source_lock.return_value.release.assert_called_once_with()
    assert_equal_command_evaluations(
        command_evaluation,
        CommandEvaluation(
            command=command,
            execution_duration=execution_duration,
            success=True,
            captured_output=[stdout_line],
        ),
    )
    mock_async_create_subprocess.assert_called_once_with(
        COMMAND1,
        SOURCE1,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=environ,
    )
    (
        stdout_mock,
        stderr_mock,
    ) = mock_async_create_subprocess.return_value.communicate.return_value
    stdout_mock.decode.assert_called_once_with("utf-8")
    stderr_mock.decode.assert_called_once_with("utf-8")


@pytest.mark.asyncio
async def test_command_execute_with_two_lines_stdout(
    mock_async_create_subprocess, mock_get_source_lock, environ, mock_time
):
    stdout = ["This is a line", "This is also a line"]
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    set_async_subprocess_response(
        mock_async_create_subprocess,
        exit_code=0,
        stdout="\n".join(stdout),
        stderr="",
    )

    execution_duration = set_execution_duration(mock_time)

    command_evaluation = await command.execute_async(source)

    mock_get_source_lock.assert_awaited_once_with(SOURCE1)
    mock_get_source_lock.return_value.acquire.assert_awaited_once_with()
    mock_get_source_lock.return_value.release.assert_called_once_with()
    assert_equal_command_evaluations(
        command_evaluation,
        CommandEvaluation(
            command=command,
            execution_duration=execution_duration,
            success=True,
            captured_output=stdout,
        ),
    )
    mock_async_create_subprocess.assert_called_once_with(
        COMMAND1,
        SOURCE1,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=environ,
    )
    (
        stdout_mock,
        stderr_mock,
    ) = mock_async_create_subprocess.return_value.communicate.return_value
    stdout_mock.decode.assert_called_once_with("utf-8")
    stderr_mock.decode.assert_called_once_with("utf-8")


@pytest.mark.asyncio
async def test_command_execute_with_one_line_stderr(
    mock_async_create_subprocess, mock_get_source_lock, environ, mock_time
):
    stderr_line = "This is a line"
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    set_async_subprocess_response(
        mock_async_create_subprocess, exit_code=0, stdout="", stderr=stderr_line
    )

    execution_duration = set_execution_duration(mock_time)

    command_evaluation = await command.execute_async(source)

    mock_get_source_lock.assert_awaited_once_with(SOURCE1)
    mock_get_source_lock.return_value.acquire.assert_awaited_once_with()
    mock_get_source_lock.return_value.release.assert_called_once_with()
    assert_equal_command_evaluations(
        command_evaluation,
        CommandEvaluation(
            command=command,
            execution_duration=execution_duration,
            success=True,
            captured_output=[stderr_line],
        ),
    )
    mock_async_create_subprocess.assert_called_once_with(
        COMMAND1,
        SOURCE1,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=environ,
    )
    (
        stdout_mock,
        stderr_mock,
    ) = mock_async_create_subprocess.return_value.communicate.return_value
    stdout_mock.decode.assert_called_once_with("utf-8")
    stderr_mock.decode.assert_called_once_with("utf-8")


@pytest.mark.asyncio
async def test_command_execute_with_two_lines_stderr(
    mock_async_create_subprocess, mock_get_source_lock, environ, mock_time
):
    stderr = ["This is a line", "This is also a line"]
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    set_async_subprocess_response(
        mock_async_create_subprocess,
        exit_code=0,
        stdout="",
        stderr="\n".join(stderr),
    )

    execution_duration = set_execution_duration(mock_time)

    command_evaluation = await command.execute_async(source)

    mock_get_source_lock.assert_awaited_once_with(SOURCE1)
    mock_get_source_lock.return_value.acquire.assert_awaited_once_with()
    mock_get_source_lock.return_value.release.assert_called_once_with()
    assert_equal_command_evaluations(
        command_evaluation,
        CommandEvaluation(
            command=command,
            execution_duration=execution_duration,
            success=True,
            captured_output=stderr,
        ),
    )
    mock_async_create_subprocess.assert_called_once_with(
        COMMAND1,
        SOURCE1,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=environ,
    )
    (
        stdout_mock,
        stderr_mock,
    ) = mock_async_create_subprocess.return_value.communicate.return_value
    stdout_mock.decode.assert_called_once_with("utf-8")
    stderr_mock.decode.assert_called_once_with("utf-8")


@pytest.mark.asyncio
async def test_command_execute_with_both_stdout_and_stderr(
    mock_async_create_subprocess, mock_get_source_lock, environ, mock_time
):
    stdout_line, stderr_line = "This is an stdout line", "This is an stderr line"
    source = SOURCE1
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    set_async_subprocess_response(
        mock_async_create_subprocess,
        exit_code=0,
        stdout=stdout_line + "\n",
        stderr=stderr_line,
    )

    execution_duration = set_execution_duration(mock_time)

    command_evaluation = await command.execute_async(source)

    mock_get_source_lock.assert_awaited_once_with(SOURCE1)
    mock_get_source_lock.return_value.acquire.assert_awaited_once_with()
    mock_get_source_lock.return_value.release.assert_called_once_with()
    assert_equal_command_evaluations(
        command_evaluation,
        CommandEvaluation(
            command=command,
            execution_duration=execution_duration,
            success=True,
            captured_output=[stdout_line, stderr_line],
        ),
    )
    mock_async_create_subprocess.assert_called_once_with(
        COMMAND1,
        SOURCE1,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        env=environ,
    )
    (
        stdout_mock,
        stderr_mock,
    ) = mock_async_create_subprocess.return_value.communicate.return_value
    stdout_mock.decode.assert_called_once_with("utf-8")
    stderr_mock.decode.assert_called_once_with("utf-8")


@pytest.mark.asyncio
async def test_command_execute_raises_file_not_found_exception(mock_subprocess):
    mock_async_create_subprocess.side_effect = FileNotFoundError
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    source = SOURCE1
    with pytest.raises(
        CommandExecutionError,
        match=f'^Cannot execute "{COMMAND1}" because it is not installed.$',
    ):
        await command.execute_async(source)
