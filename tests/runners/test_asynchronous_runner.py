import mock
import pytest

from statue.commands_map import CommandsMap
from statue.runner import AsynchronousEvaluationRunner
from tests.constants import EPSILON, SOURCE1, SOURCE2
from tests.util import set_execution_duration


@pytest.mark.asyncio
async def test_asynchronous_runner_evaluate_command():
    command_evaluation = mock.Mock()
    command = mock.Mock()
    command.execute_async = mock.AsyncMock(return_value=command_evaluation)
    evaluation = mock.MagicMock()
    runner = AsynchronousEvaluationRunner()

    with mock.patch.object(runner, "update_lock") as update_lock_mock:
        update_lock_mock.acquire = mock.AsyncMock()
        await runner.evaluate_command(
            command=command, source=SOURCE1, evaluation=evaluation
        )
        update_lock_mock.acquire.assert_awaited_once_with()
        update_lock_mock.release.assert_called_once_with()
    evaluation.__getitem__.assert_called_once_with(SOURCE1)
    evaluation.__getitem__.return_value.append.assert_called_once_with(
        command_evaluation
    )


@pytest.mark.asyncio
async def test_asynchronous_runner_evaluate_command_with_update_func():
    command_evaluation = mock.Mock()
    command = mock.Mock()
    command.execute_async = mock.AsyncMock(return_value=command_evaluation)
    evaluation = mock.MagicMock()
    runner = AsynchronousEvaluationRunner()
    update_func = mock.Mock()

    with mock.patch.object(runner, "update_lock") as update_lock_mock:
        update_lock_mock.acquire = mock.AsyncMock()
        await runner.evaluate_command(
            command=command,
            source=SOURCE1,
            evaluation=evaluation,
            update_func=update_func,
        )
        update_lock_mock.acquire.assert_awaited_once_with()
        update_lock_mock.release.assert_called_once_with()
    update_func.assert_called_once_with(evaluation)
    evaluation.__getitem__.assert_called_once_with(SOURCE1)
    evaluation.__getitem__.return_value.append.assert_called_once_with(
        command_evaluation
    )


@pytest.mark.asyncio
async def test_asynchronous_runner_evaluate_source(mock_time):
    expected_execution_duration = set_execution_duration(mock_time)
    command1, command2 = mock.Mock(), mock.Mock()
    evaluation = mock.MagicMock()
    runner = AsynchronousEvaluationRunner()

    with mock.patch.object(
        runner, "evaluate_command", new_callable=mock.AsyncMock
    ) as evaluate_command_mock:
        await runner.evaluate_source(
            commands=[command1, command2], source=SOURCE1, evaluation=evaluation
        )
        assert evaluate_command_mock.await_count == 2
        assert evaluate_command_mock.await_args_list == [
            mock.call(
                command=command1,
                source=SOURCE1,
                evaluation=evaluation,
                update_func=None,
            ),
            mock.call(
                command=command2,
                source=SOURCE1,
                evaluation=evaluation,
                update_func=None,
            ),
        ]
    evaluation.__getitem__.assert_called_once_with(SOURCE1)
    execution_duration = evaluation.__getitem__.return_value.source_execution_duration
    assert execution_duration == pytest.approx(expected_execution_duration, rel=EPSILON)


@pytest.mark.asyncio
async def test_asynchronous_runner_evaluate_source_with_update_func(mock_time):
    expected_execution_duration = set_execution_duration(mock_time)
    command1, command2 = mock.Mock(), mock.Mock()
    evaluation = mock.MagicMock()
    runner = AsynchronousEvaluationRunner()
    update_func = mock.Mock()

    with mock.patch.object(
        runner, "evaluate_command", new_callable=mock.AsyncMock
    ) as evaluate_command_mock:
        await runner.evaluate_source(
            commands=[command1, command2],
            source=SOURCE1,
            evaluation=evaluation,
            update_func=update_func,
        )
        assert evaluate_command_mock.await_count == 2
        assert evaluate_command_mock.await_args_list == [
            mock.call(
                command=command1,
                source=SOURCE1,
                evaluation=evaluation,
                update_func=update_func,
            ),
            mock.call(
                command=command2,
                source=SOURCE1,
                evaluation=evaluation,
                update_func=update_func,
            ),
        ]
    evaluation.__getitem__.assert_called_once_with(SOURCE1)
    execution_duration = evaluation.__getitem__.return_value.source_execution_duration
    assert execution_duration == pytest.approx(expected_execution_duration, rel=EPSILON)


@pytest.mark.asyncio
async def test_asynchronous_runner_evaluate_commands_map(mock_time):
    expected_execution_duration = set_execution_duration(mock_time)
    command1, command2, command3 = mock.Mock(), mock.Mock(), mock.Mock()
    commands_map = CommandsMap({SOURCE1: [command1], SOURCE2: [command2, command3]})
    runner = AsynchronousEvaluationRunner()

    with mock.patch.object(
        runner, "evaluate_source", new_callable=mock.AsyncMock
    ) as evaluate_source_mock:
        evaluation = await runner.evaluate_commands_map(commands_map=commands_map)
        assert evaluate_source_mock.await_count == 2
        assert evaluate_source_mock.await_args_list == [
            mock.call(
                commands=[command1],
                source=SOURCE1,
                evaluation=evaluation,
                update_func=None,
            ),
            mock.call(
                commands=[command2, command3],
                source=SOURCE2,
                evaluation=evaluation,
                update_func=None,
            ),
        ]
    assert evaluation.total_execution_duration == pytest.approx(
        expected_execution_duration, rel=EPSILON
    )


@pytest.mark.asyncio
async def test_asynchronous_runner_evaluate_commands_map_with_update_func(mock_time):
    expected_execution_duration = set_execution_duration(mock_time)
    command1, command2, command3 = mock.Mock(), mock.Mock(), mock.Mock()
    commands_map = CommandsMap({SOURCE1: [command1], SOURCE2: [command2, command3]})
    update_func = mock.Mock()
    runner = AsynchronousEvaluationRunner()

    with mock.patch.object(
        runner, "evaluate_source", new_callable=mock.AsyncMock
    ) as evaluate_source_mock:
        evaluation = await runner.evaluate_commands_map(
            commands_map=commands_map, update_func=update_func
        )
        assert evaluate_source_mock.await_count == 2
        assert evaluate_source_mock.await_args_list == [
            mock.call(
                commands=[command1],
                source=SOURCE1,
                evaluation=evaluation,
                update_func=update_func,
            ),
            mock.call(
                commands=[command2, command3],
                source=SOURCE2,
                evaluation=evaluation,
                update_func=update_func,
            ),
        ]
    assert evaluation.total_execution_duration == pytest.approx(
        expected_execution_duration, rel=EPSILON
    )


def test_asynchronous_runner_evaluate(event_loop):
    commands_map = mock.Mock()
    runner = AsynchronousEvaluationRunner()

    with mock.patch.object(
        runner, "evaluate_commands_map", new_callable=mock.AsyncMock
    ) as evaluate_commands_map_mock:
        evaluation = runner.evaluate(commands_map=commands_map)
        assert evaluation == evaluate_commands_map_mock.return_value
        evaluate_commands_map_mock.assert_awaited_once_with(
            commands_map=commands_map, update_func=None
        )


def test_asynchronous_runner_evaluate_with_update_func(event_loop):
    commands_map = mock.Mock()
    update_func = mock.Mock()
    runner = AsynchronousEvaluationRunner()

    with mock.patch.object(
        runner, "evaluate_commands_map", new_callable=mock.AsyncMock
    ) as evaluate_commands_map_mock:
        evaluation = runner.evaluate(commands_map=commands_map, update_func=update_func)
        assert evaluation == evaluate_commands_map_mock.return_value
        evaluate_commands_map_mock.assert_awaited_once_with(
            commands_map=commands_map, update_func=update_func
        )
