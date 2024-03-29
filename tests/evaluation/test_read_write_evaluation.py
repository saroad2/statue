import datetime
import random
from pathlib import Path
from unittest import mock

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.command import Command
from statue.constants import DATETIME_FORMAT
from statue.evaluation import CommandEvaluation, Evaluation, SourceEvaluation
from tests.constants import (
    ARG1,
    ARG2,
    COMMAND1,
    COMMAND2,
    COMMAND_CAPTURED_OUTPUT1,
    COMMAND_CAPTURED_OUTPUT2,
    SOURCE1,
    SOURCE2,
)


def case_empty():
    evaluation_json = dict(
        timestamp=datetime.datetime.now().strftime(DATETIME_FORMAT),
        sources_evaluations={},
        total_execution_duration=0,
    )
    evaluation = Evaluation()
    return evaluation_json, evaluation


def case_with_predefined_datetime():
    evaluation_json = dict(
        timestamp="05/15/1984, 15:18:20",
        sources_evaluations={},
        total_execution_duration=0,
    )
    evaluation = Evaluation(
        timestamp=datetime.datetime(
            year=1984, month=5, day=15, hour=15, minute=18, second=20
        )
    )
    return evaluation_json, evaluation


def case_one_source_no_commands():
    evaluation_json = dict(
        timestamp=datetime.datetime.now().strftime(DATETIME_FORMAT),
        sources_evaluations={
            SOURCE1: dict(commands_evaluations=[], source_execution_duration=0)
        },
        total_execution_duration=0,
    )
    evaluation = Evaluation()
    evaluation[Path(SOURCE1)] = SourceEvaluation()
    return evaluation_json, evaluation


def case_one_source_one_commands():
    command_execution_duration, source_execution_duration, total_execution_duration = (
        random.random(),
        random.random(),
        random.random(),
    )
    evaluation_json = dict(
        timestamp=datetime.datetime.now().strftime(DATETIME_FORMAT),
        total_execution_duration=total_execution_duration,
        sources_evaluations={
            SOURCE1: dict(
                source_execution_duration=source_execution_duration,
                commands_evaluations=[
                    dict(
                        command=dict(name=COMMAND1, args=[]),
                        captured_output=COMMAND_CAPTURED_OUTPUT1,
                        execution_duration=command_execution_duration,
                        success=True,
                    )
                ],
            )
        },
    )
    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[Path(SOURCE1)] = SourceEvaluation(
        commands_evaluations=[
            CommandEvaluation(
                command=Command(COMMAND1),
                captured_output=COMMAND_CAPTURED_OUTPUT1,
                execution_duration=command_execution_duration,
                success=True,
            )
        ],
        source_execution_duration=source_execution_duration,
    )
    return evaluation_json, evaluation


def case_one_source_two_commands():
    (
        command_execution_duration1,
        command_execution_duration2,
        source_execution_duration,
        total_execution_duration,
    ) = (random.random(), random.random(), random.random(), random.random())
    evaluation_json = dict(
        timestamp=datetime.datetime.now().strftime(DATETIME_FORMAT),
        total_execution_duration=total_execution_duration,
        sources_evaluations={
            SOURCE1: dict(
                source_execution_duration=source_execution_duration,
                commands_evaluations=[
                    dict(
                        command=dict(name=COMMAND1, args=[]),
                        captured_output=COMMAND_CAPTURED_OUTPUT1,
                        execution_duration=command_execution_duration1,
                        success=True,
                    ),
                    dict(
                        command=dict(name=COMMAND2, args=[ARG1, ARG2]),
                        captured_output=COMMAND_CAPTURED_OUTPUT2,
                        execution_duration=command_execution_duration2,
                        success=False,
                    ),
                ],
            )
        },
    )
    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[Path(SOURCE1)] = SourceEvaluation(
        source_execution_duration=source_execution_duration,
        commands_evaluations=[
            CommandEvaluation(
                command=Command(COMMAND1),
                captured_output=COMMAND_CAPTURED_OUTPUT1,
                execution_duration=command_execution_duration1,
                success=True,
            ),
            CommandEvaluation(
                command=Command(COMMAND2, args=[ARG1, ARG2]),
                captured_output=COMMAND_CAPTURED_OUTPUT2,
                execution_duration=command_execution_duration2,
                success=False,
            ),
        ],
    )
    return evaluation_json, evaluation


def case_two_sources_two_commands():
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
    evaluation_json = dict(
        timestamp=datetime.datetime.now().strftime(DATETIME_FORMAT),
        total_execution_duration=total_execution_duration,
        sources_evaluations={
            SOURCE1: dict(
                source_execution_duration=source_execution_duration1,
                commands_evaluations=[
                    dict(
                        command=dict(name=COMMAND1, args=[]),
                        captured_output=COMMAND_CAPTURED_OUTPUT1,
                        execution_duration=command_execution_duration1,
                        success=True,
                    )
                ],
            ),
            SOURCE2: dict(
                source_execution_duration=source_execution_duration2,
                commands_evaluations=[
                    dict(
                        command=dict(name=COMMAND2, args=[ARG1, ARG2]),
                        captured_output=COMMAND_CAPTURED_OUTPUT2,
                        execution_duration=command_execution_duration2,
                        success=False,
                    )
                ],
            ),
        },
    )
    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[Path(SOURCE1)] = SourceEvaluation(
        source_execution_duration=source_execution_duration1,
        commands_evaluations=[
            CommandEvaluation(
                command=Command(COMMAND1),
                captured_output=COMMAND_CAPTURED_OUTPUT1,
                execution_duration=command_execution_duration1,
                success=True,
            ),
        ],
    )
    evaluation[Path(SOURCE2)] = SourceEvaluation(
        source_execution_duration=source_execution_duration2,
        commands_evaluations=[
            CommandEvaluation(
                command=Command(COMMAND2, args=[ARG1, ARG2]),
                captured_output=COMMAND_CAPTURED_OUTPUT2,
                execution_duration=command_execution_duration2,
                success=False,
            ),
        ],
    )
    return evaluation_json, evaluation


@parametrize_with_cases(argnames=["evaluation_json", "evaluation"], cases=THIS_MODULE)
def test_evaluation_from_dict(evaluation_json, evaluation):
    assert evaluation == Evaluation.from_dict(evaluation_json)


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
def test_evaluation_as_dict(evaluation_json, evaluation):
    assert evaluation_json == evaluation.as_dict()


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
        assert evaluation[source] == SourceEvaluation.from_dict(
            evaluation_json["sources_evaluations"][source.as_posix()]
        )
