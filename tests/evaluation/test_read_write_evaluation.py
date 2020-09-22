from pathlib import Path
from unittest import mock

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.command import Command
from statue.evaluation import Evaluation, SourceEvaluation, CommandEvaluation
from tests.constants import (
    SOURCE1,
    COMMAND1,
    COMMAND_HELP_STRING1,
    COMMAND2,
    COMMAND_HELP_STRING2,
    ARG1,
    ARG2,
    SOURCE2,
)


def case_empty():
    evaluation_json = {}
    evaluation = Evaluation()
    return evaluation_json, evaluation


def case_one_source_no_commands():
    evaluation_json = {SOURCE1: []}
    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation()
    return evaluation_json, evaluation


def case_one_source_one_commands():
    evaluation_json = {
        SOURCE1: [
            dict(
                command=dict(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]),
                success=True,
            )
        ]
    }
    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(
                command=Command(COMMAND1, help=COMMAND_HELP_STRING1), success=True
            )
        ]
    )
    return evaluation_json, evaluation


def case_one_source_two_commands():
    evaluation_json = {
        SOURCE1: [
            dict(
                command=dict(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]),
                success=True,
            ),
            dict(
                command=dict(
                    name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG1, ARG2]
                ),
                success=False,
            ),
        ]
    }
    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(
                command=Command(COMMAND1, help=COMMAND_HELP_STRING1), success=True
            ),
            CommandEvaluation(
                command=Command(COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG1, ARG2]),
                success=False,
            ),
        ]
    )
    return evaluation_json, evaluation


def case_two_sources_two_commands():
    evaluation_json = {
        SOURCE1: [
            dict(
                command=dict(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]),
                success=True,
            )
        ],
        SOURCE2: [
            dict(
                command=dict(
                    name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG1, ARG2]
                ),
                success=False,
            )
        ],
    }
    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(
                command=Command(COMMAND1, help=COMMAND_HELP_STRING1), success=True
            ),
        ]
    )
    evaluation[SOURCE2] = SourceEvaluation(
        [
            CommandEvaluation(
                command=Command(COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG1, ARG2]),
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
            mock_open.assert_called_once_with(file_path, mode="r")
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
            mock_open.assert_called_once_with(file_path, mode="w")
            mock_json.dump.assert_called_once_with(
                evaluation_json, mock_open.return_value, indent=2
            )


@parametrize_with_cases(argnames=["evaluation_json", "evaluation"], cases=THIS_MODULE)
def test_iterate_evaluation(evaluation_json, evaluation):
    for source in evaluation:
        assert evaluation[source] == SourceEvaluation.from_json(evaluation_json[source])
