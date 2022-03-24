import random

import mock
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.commands_map import CommandsMap
from statue.constants import BAR_FORMAT
from statue.evaluation import CommandEvaluation, Evaluation, SourceEvaluation
from statue.runner import SynchronousEvaluationRunner
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND_CAPTURED_OUTPUT1,
    COMMAND_CAPTURED_OUTPUT2,
    COMMAND_CAPTURED_OUTPUT3,
    SOURCE1,
    SOURCE2,
)
from tests.util import assert_equal_evaluations, command_mock


def tqdm_side_effect(items, *args, **kwargs):
    return items


def case_empty_commands_map(mock_time):
    mock_time.side_effect = [0, 0]
    commands_map = CommandsMap()
    evaluation = Evaluation()
    return commands_map, evaluation, []


def case_one_source_one_command(mock_time):
    command_execution_duration, source_execution_duration, total_execution_duration = (
        random.random(),
        random.random(),
        random.random(),
    )
    source_start_time, total_start_time = random.random(), random.random()
    mock_time.side_effect = [
        total_start_time,
        source_start_time,
        source_start_time + source_execution_duration,
        total_start_time + total_execution_duration,
    ]
    command1 = command_mock(
        COMMAND1,
        execution_duration=command_execution_duration,
        captured_output=COMMAND_CAPTURED_OUTPUT1,
    )
    commands_map = CommandsMap({SOURCE1: [command1]})

    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[SOURCE1] = SourceEvaluation(
        source_execution_duration=source_execution_duration,
        commands_evaluations=[
            CommandEvaluation(
                command=command1,
                execution_duration=command_execution_duration,
                success=True,
                captured_output=COMMAND_CAPTURED_OUTPUT1,
            )
        ],
    )
    return commands_map, evaluation


def case_one_source_two_commands(mock_time):
    (
        command_execution_duration1,
        command_execution_duration2,
        source_execution_duration,
        total_execution_duration,
    ) = (random.random(), random.random(), random.random(), random.random())
    source_start_time, total_start_time = random.random(), random.random()
    mock_time.side_effect = [
        total_start_time,
        source_start_time,
        source_start_time + source_execution_duration,
        total_start_time + total_execution_duration,
    ]
    command1 = command_mock(
        COMMAND1,
        execution_duration=command_execution_duration1,
        captured_output=COMMAND_CAPTURED_OUTPUT1,
    )
    command2 = command_mock(
        COMMAND2,
        execution_duration=command_execution_duration2,
        success=False,
        captured_output=COMMAND_CAPTURED_OUTPUT2,
    )
    commands_map = CommandsMap({SOURCE1: [command1, command2]})

    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[SOURCE1] = SourceEvaluation(
        source_execution_duration=source_execution_duration,
        commands_evaluations=[
            CommandEvaluation(
                command=command1,
                execution_duration=command_execution_duration1,
                success=True,
                captured_output=COMMAND_CAPTURED_OUTPUT1,
            ),
            CommandEvaluation(
                command=command2,
                execution_duration=command_execution_duration2,
                success=False,
                captured_output=COMMAND_CAPTURED_OUTPUT2,
            ),
        ],
    )

    return commands_map, evaluation


def case_one_source_three_commands(mock_time):
    (
        command_execution_duration1,
        command_execution_duration2,
        command_execution_duration3,
        source_execution_duration,
        total_execution_duration,
    ) = (
        random.random(),
        random.random(),
        random.random(),
        random.random(),
        random.random(),
    )
    source_start_time, total_start_time = random.random(), random.random()
    mock_time.side_effect = [
        total_start_time,
        source_start_time,
        source_start_time + source_execution_duration,
        total_start_time + total_execution_duration,
    ]
    command1 = command_mock(
        COMMAND1,
        execution_duration=command_execution_duration1,
        captured_output=COMMAND_CAPTURED_OUTPUT1,
    )
    command2 = command_mock(
        COMMAND2,
        execution_duration=command_execution_duration2,
        success=False,
        captured_output=COMMAND_CAPTURED_OUTPUT2,
    )
    command3 = command_mock(
        COMMAND3,
        execution_duration=command_execution_duration3,
        success=False,
        captured_output=COMMAND_CAPTURED_OUTPUT3,
    )
    commands_map = CommandsMap({SOURCE1: [command1, command2, command3]})

    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[SOURCE1] = SourceEvaluation(
        source_execution_duration=source_execution_duration,
        commands_evaluations=[
            CommandEvaluation(
                command=command1,
                execution_duration=command_execution_duration1,
                success=True,
                captured_output=COMMAND_CAPTURED_OUTPUT1,
            ),
            CommandEvaluation(
                command=command2,
                success=False,
                execution_duration=command_execution_duration2,
                captured_output=COMMAND_CAPTURED_OUTPUT2,
            ),
            CommandEvaluation(
                command=command3,
                execution_duration=command_execution_duration3,
                success=False,
                captured_output=COMMAND_CAPTURED_OUTPUT3,
            ),
        ],
    )
    return commands_map, evaluation


def case_two_sources_two_commands(mock_time):
    (
        command_execution_duration1,
        command_execution_duration2,
        source_execution_duration1,
        source_execution_duration2,
        total_execution_duration,
    ) = (
        random.random(),
        random.random(),
        random.random(),
        random.random(),
        random.random(),
    )
    source_start_time1, source_start_time2, total_start_time = (
        random.random(),
        random.random(),
        random.random(),
    )
    mock_time.side_effect = [
        total_start_time,
        source_start_time1,
        source_start_time1 + source_execution_duration1,
        source_start_time2,
        source_start_time2 + source_execution_duration2,
        total_start_time + total_execution_duration,
    ]
    command1 = command_mock(
        COMMAND1,
        execution_duration=command_execution_duration1,
        captured_output=COMMAND_CAPTURED_OUTPUT1,
    )
    command2 = command_mock(
        COMMAND2,
        execution_duration=command_execution_duration2,
        success=False,
        captured_output=COMMAND_CAPTURED_OUTPUT2,
    )
    commands_map = CommandsMap({SOURCE1: [command1], SOURCE2: [command2]})

    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[SOURCE1] = SourceEvaluation(
        source_execution_duration=source_execution_duration1,
        commands_evaluations=[
            CommandEvaluation(
                command=command1,
                execution_duration=command_execution_duration1,
                success=True,
                captured_output=COMMAND_CAPTURED_OUTPUT1,
            )
        ],
    )
    evaluation[SOURCE2] = SourceEvaluation(
        source_execution_duration=source_execution_duration2,
        commands_evaluations=[
            CommandEvaluation(
                command=command2,
                execution_duration=command_execution_duration2,
                success=False,
                captured_output=COMMAND_CAPTURED_OUTPUT2,
            )
        ],
    )

    return commands_map, evaluation


@parametrize_with_cases(argnames=["commands_map", "evaluation"], cases=THIS_MODULE)
def test_evaluate_commands_map_result(
    commands_map, evaluation, mock_tqdm, mock_tqdm_range
):
    runner = SynchronousEvaluationRunner()
    mock_tqdm.side_effect = tqdm_side_effect
    actual_evaluation = runner.evaluate(commands_map)
    assert_equal_evaluations(actual_evaluation, evaluation)
    mock_tqdm_range.assert_called_once_with(
        commands_map.total_commands_count,
        bar_format=BAR_FORMAT,
        colour="blue",
    )
    assert mock_tqdm.call_count == len(commands_map)
    for i, key in enumerate(commands_map.keys()):
        assert mock_tqdm.call_args_list[i] == mock.call(
            commands_map[key],
            bar_format=BAR_FORMAT,
            colour="yellow",
            leave=False,
            desc=key,
        )
