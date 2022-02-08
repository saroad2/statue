import random

import click
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli.string_util import evaluation_string
from statue.command import CommandEvaluation
from statue.evaluation import Evaluation, SourceEvaluation
from statue.verbosity import VERBOSE
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND_CAPTURED_OUTPUT1,
    COMMAND_CAPTURED_OUTPUT2,
    SOURCE1,
    SOURCE2,
)
from tests.util import command_mock


def case_empty_evaluation():
    evaluation = Evaluation()
    kwargs = {}
    result = ""
    return evaluation, kwargs, result


def case_one_source_one_command():
    evaluation = Evaluation(
        {
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=command_mock(COMMAND1),
                        execution_duration=random.random(),
                        success=True,
                        captured_output=COMMAND_CAPTURED_OUTPUT1,
                    )
                ]
            )
        }
    )
    kwargs = {}
    joined_output = "\n".join(COMMAND_CAPTURED_OUTPUT1)
    result = (
        "\n\n"
        "source1\n"
        "=======\n"
        "\n"
        "command1\n"
        "--------\n"
        f"{joined_output}\n"
    )
    return evaluation, kwargs, result


def case_one_source_two_commands():
    evaluation = Evaluation(
        {
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=command_mock(COMMAND1),
                        execution_duration=random.random(),
                        success=True,
                        captured_output=COMMAND_CAPTURED_OUTPUT1,
                    ),
                    CommandEvaluation(
                        command=command_mock(COMMAND2),
                        execution_duration=random.random(),
                        success=True,
                        captured_output=COMMAND_CAPTURED_OUTPUT2,
                    ),
                ]
            )
        }
    )
    kwargs = {}
    joined_command1_output = "\n".join(COMMAND_CAPTURED_OUTPUT1)
    joined_command2_output = "\n".join(COMMAND_CAPTURED_OUTPUT2)
    result = (
        "\n\n"
        "source1\n"
        "=======\n"
        "\n"
        "command1\n"
        "--------\n"
        f"{joined_command1_output}\n"
        "command2\n"
        "--------\n"
        f"{joined_command2_output}\n"
    )
    return evaluation, kwargs, result


def case_two_sources_two_commands():
    evaluation = Evaluation(
        {
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=command_mock(COMMAND1),
                        execution_duration=random.random(),
                        success=True,
                        captured_output=COMMAND_CAPTURED_OUTPUT1,
                    )
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=command_mock(COMMAND2),
                        execution_duration=random.random(),
                        success=True,
                        captured_output=COMMAND_CAPTURED_OUTPUT2,
                    )
                ]
            ),
        }
    )
    kwargs = {}
    joined_command1_output = "\n".join(COMMAND_CAPTURED_OUTPUT1)
    joined_command2_output = "\n".join(COMMAND_CAPTURED_OUTPUT2)
    result = (
        "\n\n"
        "source1\n"
        "=======\n\n"
        "command1\n"
        "--------\n"
        f"{joined_command1_output}\n\n\n"
        "source2\n"
        "=======\n\n"
        "command2\n"
        "--------\n"
        f"{joined_command2_output}\n"
    )
    return evaluation, kwargs, result


def case_evaluation_string_verbose():
    execution_duration = 0.25
    evaluation = Evaluation(
        {
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=command_mock(COMMAND1, args=["a", "b", "c"]),
                        execution_duration=execution_duration,
                        success=True,
                        captured_output=COMMAND_CAPTURED_OUTPUT1,
                    )
                ]
            )
        }
    )
    kwargs = dict(verbosity=VERBOSE)
    joined_command_output = "\n".join(COMMAND_CAPTURED_OUTPUT1)
    result = (
        "\n\n"
        "source1\n"
        "=======\n"
        "\n"
        "command1\n"
        "--------\n"
        "command1 ran with args: ['a', 'b', 'c']\n"
        "Finished in 0.25 seconds.\n"
        f"{joined_command_output}\n"
    )
    return evaluation, kwargs, result


@parametrize_with_cases(["evaluation", "kwargs", "result"], cases=THIS_MODULE)
def test_evaluation_string(evaluation, kwargs, result):
    assert result == click.unstyle(evaluation_string(evaluation=evaluation, **kwargs))
