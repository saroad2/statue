import datetime
import random
from typing import Optional
from unittest import mock

import pytest

from statue.command import Command, CommandEvaluation
from statue.command_builder import CommandBuilder
from statue.evaluation import Evaluation, SourceEvaluation
from tests.constants import EPSILON


def dummy_version():
    major, minor, patch = (
        random.randint(0, 10),
        random.randint(0, 10),
        random.randint(0, 10),
    )
    return f"{major}.{minor}.{patch}"


def build_commands_builders_map(*commands_builders: CommandBuilder):
    return {
        commands_builders.name: commands_builders
        for commands_builders in commands_builders
    }


def build_failure_evaluation(commands_map):
    return Evaluation(
        sources_evaluations={
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
    name, execution_duration=0, success=True, args=None, captured_output=None
):
    command = Command(name=name, args=args)
    command_evaluation = CommandEvaluation(
        command=command,
        success=success,
        execution_duration=execution_duration,
        captured_output=[] if captured_output is None else captured_output,
    )
    command.execute = mock.Mock(return_value=command_evaluation)
    return command


def command_builder_mock(
    name,
    version=None,
    default_args=None,
    installed=True,
    installed_version="0.0.1",
):
    default_args = default_args if default_args is not None else []
    command_builder = CommandBuilder(
        name=name, help="This is help", version=version, default_args=default_args
    )
    command_builder.build_command = mock.Mock(return_value=command_mock(name=name))
    command_builder.update_from_config = mock.Mock()
    get_package = mock.Mock()
    if not installed:
        get_package.return_value = None
    else:
        get_package.return_value.version = installed_version
    command_builder._get_package = get_package  # pylint: disable=protected-access
    command_builder.install = mock.Mock()
    command_builder.update = mock.Mock()
    command_builder.update_to_version = mock.Mock()
    command_builder.as_dict = mock.Mock()
    return command_builder


def evaluation_mock(
    successful_commands: int,
    total_commands: int,
    total_execution_duration: float,
    timestamp: Optional[datetime.datetime] = None,
):
    evaluation = mock.Mock()
    evaluation.successful_commands_number = successful_commands
    evaluation.commands_number = total_commands
    evaluation.success = successful_commands == total_commands
    evaluation.total_execution_duration = total_execution_duration
    evaluation.timestamp = (
        timestamp if timestamp is not None else datetime.datetime.now()
    )
    return evaluation


def successful_evaluation_mock(
    total_commands: Optional[int] = None,
    total_execution_duration: Optional[float] = None,
    timestamp: Optional[datetime.datetime] = None,
):
    if total_commands is None:
        total_commands = random.randint(1, 10)
    if total_execution_duration is None:
        total_execution_duration = random.uniform(0, 100)
    return evaluation_mock(
        successful_commands=total_commands,
        total_commands=total_commands,
        total_execution_duration=total_execution_duration,
        timestamp=timestamp,
    )


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
