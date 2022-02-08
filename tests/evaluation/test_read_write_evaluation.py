import random
from pathlib import Path
from unittest import mock

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.command import Command
from statue.evaluation import CommandEvaluation, Evaluation, SourceEvaluation
from tests.constants import (
    ARG1,
    ARG2,
    COMMAND1,
    COMMAND2,
    COMMAND_CAPTURED_OUTPUT1,
    COMMAND_CAPTURED_OUTPUT2,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    SOURCE1,
    SOURCE2,
)


def case_empty():
    evaluation_json = {}
    evaluation = Evaluation()
    return evaluation_json, evaluation


def case_one_source_no_commands():
    evaluation_json = {SOURCE1: dict(commands_evaluations=[])}
    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation()
    return evaluation_json, evaluation


def case_one_source_one_commands():
    execution_duration = random.random()
    evaluation_json = {
        SOURCE1: dict(
            commands_evaluations=[
                dict(
                    command=dict(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]),
                    captured_output=COMMAND_CAPTURED_OUTPUT1,
                    execution_duration=execution_duration,
                    success=True,
                )
            ]
        )
    }
    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(
                command=Command(COMMAND1, help=COMMAND_HELP_STRING1),
                captured_output=COMMAND_CAPTURED_OUTPUT1,
                execution_duration=execution_duration,
                success=True,
            )
        ]
    )
    return evaluation_json, evaluation


def case_one_source_two_commands():
    execution_duration1, execution_duration2 = random.random(), random.random()
    evaluation_json = {
        SOURCE1: dict(
            commands_evaluations=[
                dict(
                    command=dict(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]),
                    captured_output=COMMAND_CAPTURED_OUTPUT1,
                    execution_duration=execution_duration1,
                    success=True,
                ),
                dict(
                    command=dict(
                        name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG1, ARG2]
                    ),
                    captured_output=COMMAND_CAPTURED_OUTPUT2,
                    execution_duration=execution_duration2,
                    success=False,
                ),
            ]
        )
    }
    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(
                command=Command(COMMAND1, help=COMMAND_HELP_STRING1),
                captured_output=COMMAND_CAPTURED_OUTPUT1,
                execution_duration=execution_duration1,
                success=True,
            ),
            CommandEvaluation(
                command=Command(COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG1, ARG2]),
                captured_output=COMMAND_CAPTURED_OUTPUT2,
                execution_duration=execution_duration2,
                success=False,
            ),
        ]
    )
    return evaluation_json, evaluation


def case_two_sources_two_commands():
    execution_duration1, execution_duration2 = random.random(), random.random()
    evaluation_json = {
        SOURCE1: dict(
            commands_evaluations=[
                dict(
                    command=dict(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]),
                    captured_output=COMMAND_CAPTURED_OUTPUT1,
                    execution_duration=execution_duration1,
                    success=True,
                )
            ]
        ),
        SOURCE2: dict(
            commands_evaluations=[
                dict(
                    command=dict(
                        name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG1, ARG2]
                    ),
                    captured_output=COMMAND_CAPTURED_OUTPUT2,
                    execution_duration=execution_duration2,
                    success=False,
                )
            ]
        ),
    }
    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(
                command=Command(COMMAND1, help=COMMAND_HELP_STRING1),
                captured_output=COMMAND_CAPTURED_OUTPUT1,
                execution_duration=execution_duration1,
                success=True,
            ),
        ]
    )
    evaluation[SOURCE2] = SourceEvaluation(
        [
            CommandEvaluation(
                command=Command(COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG1, ARG2]),
                captured_output=COMMAND_CAPTURED_OUTPUT2,
                execution_duration=execution_duration2,
                success=False,
            ),
        ]
    )
    return evaluation_json, evaluation


@parametrize_with_cases(argnames=["evaluation_json", "evaluation"], cases=THIS_MODULE)
def test_evaluation_from_json(evaluation_json, evaluation):
    assert evaluation == Evaluation.from_json(evaluation_json)


@parametrize_with_cases(argnames=["evaluation_json", "evaluation"], cases=THIS_MODULE)
def test_evaluation_load_from_file(evaluation_json, evaluation):
    file_path = Path("/path/to/data.json")
    with mock.patch("statue.evaluation.json") as mock_json:
        mock_json.load.return_value = evaluation_json
        with mock.patch("builtins.open", mock.mock_open()) as mock_open:
            assert evaluation == Evaluation.load_from_file(file_path)
            mock_open.assert_called_once_with(file_path, mode="r", encoding="utf-8")
            mock_json.load.assert_called_once_with(mock_open.return_value)


@parametrize_with_cases(argnames=["evaluation_json", "evaluation"], cases=THIS_MODULE)
def test_evaluation_as_json(evaluation_json, evaluation):
    assert evaluation_json == evaluation.as_json()


@parametrize_with_cases(argnames=["evaluation_json", "evaluation"], cases=THIS_MODULE)
def test_evaluation_save_as_json(evaluation_json, evaluation):
    file_path = Path("/path/to/data.json")
    with mock.patch("statue.evaluation.json") as mock_json:
        with mock.patch("builtins.open", mock.mock_open()) as mock_open:
            evaluation.save_as_json(file_path)
            mock_open.assert_called_once_with(file_path, mode="w", encoding="utf-8")
            mock_json.dump.assert_called_once_with(
                evaluation_json, mock_open.return_value, indent=2
            )


@parametrize_with_cases(argnames=["evaluation_json", "evaluation"], cases=THIS_MODULE)
def test_iterate_evaluation(evaluation_json, evaluation):
    for source in evaluation:
        assert evaluation[source] == SourceEvaluation.from_json(evaluation_json[source])
