from unittest.mock import Mock, call

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.evaluation import CommandEvaluation, Evaluation, SourceEvaluation
from statue.runner import evaluate_commands_map
from statue.verbosity import SILENT
from tests.constants import COMMAND1, COMMAND2, COMMAND3, SOURCE1, SOURCE2
from tests.util import assert_calls, command_mock


def case_empty_commands_map():
    commands_map = {}
    evaluation = Evaluation()
    return commands_map, evaluation, []


def case_one_source_one_command():
    command1 = command_mock(COMMAND1)
    commands_map = {SOURCE1: [command1]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [CommandEvaluation(command=command1, success=True)]
    )

    prints = [
        call(""),
        call(""),
        call("source1"),
        call("======="),
        call(""),
        call("Command1"),
        call("--------"),
    ]
    return commands_map, evaluation, prints


def case_one_source_two_commands():
    command1 = command_mock(COMMAND1)
    command2 = command_mock(COMMAND2, success=False)
    commands_map = {SOURCE1: [command1, command2]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [
            CommandEvaluation(command=command1, success=True),
            CommandEvaluation(command=command2, success=False),
        ]
    )

    prints = [
        call(""),
        call(""),
        call("source1"),
        call("======="),
        call(""),
        call("Command1"),
        call("--------"),
        call("Command2"),
        call("--------"),
    ]
    return commands_map, evaluation, prints


def case_one_source_three_commands():
    command1 = command_mock(COMMAND1)
    command2 = command_mock(COMMAND2, success=False)
    command3 = command_mock(COMMAND3, success=False)
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
        call(""),
        call(""),
        call("source1"),
        call("======="),
        call(""),
        call("Command1"),
        call("--------"),
        call("Command2"),
        call("--------"),
        call("Command3"),
        call("--------"),
    ]
    return commands_map, evaluation, prints


def case_two_sources_two_commands():
    command1 = command_mock(COMMAND1)
    command2 = command_mock(COMMAND2, success=False)
    commands_map = {SOURCE1: [command1], SOURCE2: [command2]}

    evaluation = Evaluation()
    evaluation[SOURCE1] = SourceEvaluation(
        [CommandEvaluation(command=command1, success=True)]
    )
    evaluation[SOURCE2] = SourceEvaluation(
        [CommandEvaluation(command=command2, success=False)]
    )
    prints = [
        call(""),
        call(""),
        call("source1"),
        call("======="),
        call(""),
        call("Command1"),
        call("--------"),
        call(""),
        call(""),
        call("source2"),
        call("======="),
        call(""),
        call("Command2"),
        call("--------"),
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
    assert_calls(print_mock, prints)


@parametrize_with_cases(
    argnames=["commands_map", "evaluation", "prints"], cases=THIS_MODULE
)
def test_evaluate_commands_silently(commands_map, evaluation, prints):
    print_mock = Mock()
    evaluate_commands_map(commands_map, print_method=print_mock, verbosity=SILENT)
    print_mock.assert_not_called()
