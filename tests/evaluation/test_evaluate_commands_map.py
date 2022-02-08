import itertools
import random
from unittest import mock

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.evaluation import CommandEvaluation, Evaluation, SourceEvaluation
from statue.runner import evaluate_commands_map
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
from tests.util import command_mock


def case_empty_commands_map():
    commands_map = {}
    evaluation = Evaluation()
    return commands_map, evaluation, []


def case_one_source_one_command():
    execution_duration = random.random()
    command1 = command_mock(
        COMMAND1,
        execution_duration=execution_duration,
        captured_output=COMMAND_CAPTURED_OUTPUT1,
    )
    commands_map = {SOURCE1: [command1]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(
                command=command1,
                execution_duration=execution_duration,
                success=True,
                captured_output=COMMAND_CAPTURED_OUTPUT1,
            )
        ]
    )
    return commands_map, evaluation


def case_one_source_two_commands():
    execution_duration1, execution_duration2 = random.random(), random.random()
    command1 = command_mock(
        COMMAND1,
        execution_duration=execution_duration1,
        captured_output=COMMAND_CAPTURED_OUTPUT1,
    )
    command2 = command_mock(
        COMMAND2,
        execution_duration=execution_duration2,
        success=False,
        captured_output=COMMAND_CAPTURED_OUTPUT2,
    )
    commands_map = {SOURCE1: [command1, command2]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(
                command=command1,
                execution_duration=execution_duration1,
                success=True,
                captured_output=COMMAND_CAPTURED_OUTPUT1,
            ),
            CommandEvaluation(
                command=command2,
                execution_duration=execution_duration2,
                success=False,
                captured_output=COMMAND_CAPTURED_OUTPUT2,
            ),
        ]
    )

    return commands_map, evaluation


def case_one_source_three_commands():
    execution_duration1, execution_duration2, execution_duration3 = (
        random.random(),
        random.random(),
        random.random(),
    )
    command1 = command_mock(
        COMMAND1,
        execution_duration=execution_duration1,
        captured_output=COMMAND_CAPTURED_OUTPUT1,
    )
    command2 = command_mock(
        COMMAND2,
        execution_duration=execution_duration2,
        success=False,
        captured_output=COMMAND_CAPTURED_OUTPUT2,
    )
    command3 = command_mock(
        COMMAND3,
        execution_duration=execution_duration3,
        success=False,
        captured_output=COMMAND_CAPTURED_OUTPUT3,
    )
    commands_map = {SOURCE1: [command1, command2, command3]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(
                command=command1,
                execution_duration=execution_duration1,
                success=True,
                captured_output=COMMAND_CAPTURED_OUTPUT1,
            ),
            CommandEvaluation(
                command=command2,
                success=False,
                execution_duration=execution_duration2,
                captured_output=COMMAND_CAPTURED_OUTPUT2,
            ),
            CommandEvaluation(
                command=command3,
                execution_duration=execution_duration3,
                success=False,
                captured_output=COMMAND_CAPTURED_OUTPUT3,
            ),
        ]
    )
    return commands_map, evaluation


def case_two_sources_two_commands():
    execution_duration1, execution_duration2 = random.random(), random.random()
    command1 = command_mock(
        COMMAND1,
        execution_duration=execution_duration1,
        captured_output=COMMAND_CAPTURED_OUTPUT1,
    )
    command2 = command_mock(
        COMMAND2,
        execution_duration=execution_duration2,
        success=False,
        captured_output=COMMAND_CAPTURED_OUTPUT2,
    )
    commands_map = {SOURCE1: [command1], SOURCE2: [command2]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(
                command=command1,
                execution_duration=execution_duration1,
                success=True,
                captured_output=COMMAND_CAPTURED_OUTPUT1,
            )
        ]
    )
    evaluation[SOURCE2] = SourceEvaluation(
        [
            CommandEvaluation(
                command=command2,
                execution_duration=execution_duration2,
                success=False,
                captured_output=COMMAND_CAPTURED_OUTPUT2,
            )
        ]
    )

    return commands_map, evaluation


@parametrize_with_cases(argnames=["commands_map", "evaluation"], cases=THIS_MODULE)
def test_evaluate_commands_map_result(commands_map, evaluation):
    assert evaluation == evaluate_commands_map(commands_map)


@parametrize_with_cases(argnames=["commands_map", "evaluation"], cases=THIS_MODULE)
def test_evaluate_commands_map_update_func(commands_map, evaluation):
    update_func_mock = mock.Mock()
    assert evaluation == evaluate_commands_map(
        commands_map, update_func=update_func_mock
    )
    all_commands = list(itertools.chain.from_iterable(commands_map.values()))
    assert update_func_mock.call_count == len(all_commands)
