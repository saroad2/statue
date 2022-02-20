import random
from unittest import mock

import pytest

from statue.command import Command, CommandEvaluation
from statue.evaluation import Evaluation, SourceEvaluation
from tests.constants import EPSILON


def build_contexts_map(*contexts):
    return {context.name: context for context in contexts}


def build_failure_evaluation(commands_map):
    return Evaluation(
        {
            source: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=command,
                        execution_duration=random.random(),
                        success=False,
                    )
                    for command in commands
                ]
            )
            for source, commands in commands_map.items()
        }
    )


def command_mock(
    name,
    installed=True,
    version=None,
    execution_duration=0,
    success=True,
    args=None,
    captured_output=None,
    installed_version="0.0.1",
):
    command = Command(name=name, help="This is help", version=version)
    command.name = name
    command.args = args
    command.install = mock.Mock()
    command.update = mock.Mock()
    command.update_to_version = mock.Mock()
    get_package = mock.Mock()
    if not installed:
        get_package.return_value = None
    else:
        get_package.return_value.version = installed_version
    command._get_package = get_package  # pylint: disable=protected-access
    command_evaluation = CommandEvaluation(
        command=command,
        success=success,
        execution_duration=execution_duration,
        captured_output=[] if captured_output is None else captured_output,
    )
    command.execute = mock.Mock(return_value=command_evaluation)
    return command


def evaluation_mock(successful_commands, total_commands, total_execution_duration):
    evaluation = mock.Mock()
    evaluation.successful_commands_number = successful_commands
    evaluation.commands_number = total_commands
    evaluation.success = successful_commands == total_commands
    evaluation.total_execution_duration = total_execution_duration
    return evaluation


def assert_calls(mock_obj, calls):
    assert mock_obj.call_count == len(
        calls
    ), f"Expected {len(calls)} calls, got {mock_obj.call_count}"
    for i, expected_call in enumerate(calls):
        actual_call = mock_obj.call_args_list[i]
        assert (
            actual_call == expected_call
        ), f"Call {i} is different than expected. {actual_call} != {expected_call}"


def assert_equal_command_evaluations(
    actual_evaluation: CommandEvaluation, expected_evaluation: CommandEvaluation
):
    assert actual_evaluation.command == expected_evaluation.command
    assert actual_evaluation.success == expected_evaluation.success
    assert actual_evaluation.captured_output == expected_evaluation.captured_output
    assert actual_evaluation.execution_duration == pytest.approx(
        expected_evaluation.execution_duration, rel=EPSILON
    )


def assert_equal_source_evaluations(
    actual_evaluation: SourceEvaluation, expected_evaluation: SourceEvaluation
):
    assert len(actual_evaluation.commands_evaluations) == len(
        expected_evaluation.commands_evaluations
    )
    for actual_command_evaluation, expected_command_evaluation in zip(
        actual_evaluation.commands_evaluations, expected_evaluation.commands_evaluations
    ):
        assert_equal_command_evaluations(
            actual_command_evaluation, expected_command_evaluation
        )
    assert actual_evaluation.source_execution_duration == pytest.approx(
        expected_evaluation.source_execution_duration, rel=EPSILON
    )


def assert_equal_evaluations(
    actual_evaluation: Evaluation, expected_evaluation: Evaluation
):
    assert set(actual_evaluation.keys()) == set(expected_evaluation.keys())
    for source in actual_evaluation.keys():
        assert_equal_source_evaluations(
            actual_evaluation[source], expected_evaluation[source]
        )
    assert actual_evaluation.total_execution_duration == pytest.approx(
        expected_evaluation.total_execution_duration, rel=EPSILON
    )


def set_execution_duration(mock_time):
    start_time, execution_duration = random.uniform(0, 10000), random.random()
    mock_time.side_effect = [start_time, start_time + execution_duration]
    return execution_duration
