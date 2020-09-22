from unittest.mock import call, Mock
from pytest_cases import parametrize_with_cases, THIS_MODULE

from statue.evaluation import (
    Evaluation,
    evaluate_commands_map,
    SourceEvaluation,
    CommandEvaluation,
)
from statue.verbosity import SILENT
from tests.constants import SOURCE1, COMMAND1, SOURCE2, COMMAND2, COMMAND3
from tests.util import command_mock


def case_empty_commands_map():
    commands_map = {}
    evaluation = Evaluation()
    return commands_map, evaluation, []


def case_one_source_one_command():
    command1 = command_mock(COMMAND1, return_code=0)
    commands_map = {SOURCE1: [command1]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [CommandEvaluation(command=command1, success=True)]
    )

    prints = ["", f"Evaluating {SOURCE1}", "Command1", "--------"]
    return commands_map, evaluation, prints


def case_one_source_two_commands():
    command1 = command_mock(COMMAND1, return_code=0)
    command2 = command_mock(COMMAND2, return_code=1)
    commands_map = {SOURCE1: [command1, command2]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(command=command1, success=True),
            CommandEvaluation(command=command2, success=False),
        ]
    )

    prints = [
        "",
        f"Evaluating {SOURCE1}",
        "Command1",
        "--------",
        "Command2",
        "--------",
    ]
    return commands_map, evaluation, prints


def case_one_source_three_commands():
    command1 = command_mock(COMMAND1, return_code=0)
    command2 = command_mock(COMMAND2, return_code=1)
    command3 = command_mock(COMMAND3, return_code=5)
    commands_map = {SOURCE1: [command1, command2, command3]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(command=command1, success=True),
            CommandEvaluation(command=command2, success=False),
            CommandEvaluation(command=command3, success=False),
        ]
    )
    prints = [
        "",
        f"Evaluating {SOURCE1}",
        "Command1",
        "--------",
        "Command2",
        "--------",
        "Command3",
        "--------",
    ]
    return commands_map, evaluation, prints


def case_two_sources_two_commands():
    command1 = command_mock(COMMAND1, return_code=0)
    command2 = command_mock(COMMAND2, return_code=1)
    commands_map = {SOURCE1: [command1], SOURCE2: [command2]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [CommandEvaluation(command=command1, success=True)]
    )
    evaluation[SOURCE2] = SourceEvaluation(
        [CommandEvaluation(command=command2, success=False)]
    )
    prints = [
        "",
        f"Evaluating {SOURCE1}",
        "Command1",
        "--------",
        "",
        f"Evaluating {SOURCE2}",
        "Command2",
        "--------",
    ]
    return commands_map, evaluation, prints


@parametrize_with_cases(argnames=["commands_map", "evaluation"], cases=THIS_MODULE)
def test_evaluate_commands_map_result(commands_map, evaluation):
    print_mock = Mock()
    assert evaluation == evaluate_commands_map(commands_map, print_method=print_mock)


@parametrize_with_cases(
    argnames=["commands_map", "evaluation", "prints"], cases=THIS_MODULE
)
def test_evaluate_commands_map_prints(commands_map, evaluation, prints):
    print_mock = Mock()
    evaluate_commands_map(commands_map, print_method=print_mock)
    assert print_mock.call_count == len(prints)
    for i, print_text in enumerate(prints):
        assert print_mock.call_args_list[i] == call(
            print_text
        ), f"Print call {i} is different than expected"


@parametrize_with_cases(
    argnames=["commands_map", "evaluation", "prints"], cases=THIS_MODULE
)
def test_evaluate_commands_silently(commands_map, evaluation, prints):
    print_mock = Mock()
    evaluate_commands_map(commands_map, print_method=print_mock, verbosity=SILENT)
    print_mock.assert_not_called()
