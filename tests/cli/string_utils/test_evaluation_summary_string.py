import random
from pathlib import Path

import click
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli.string_util import evaluation_summary_string
from statue.command import CommandEvaluation
from statue.evaluation import Evaluation, SourceEvaluation
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
    SOURCE1,
    SOURCE2,
    SOURCE3,
    SOURCE4,
)
from tests.util import command_mock


def case_empty_evaluation():
    total_execution_duration = 13.32
    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    expected_string = "Empty evaluation."

    return evaluation, expected_string


def case_success_one_source_one_command():
    total_execution_duration = 14.15
    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[Path(SOURCE1)] = SourceEvaluation(
        commands_evaluations=[
            CommandEvaluation(
                command=command_mock(COMMAND1),
                success=True,
                execution_duration=random.uniform(0, 100),
            )
        ],
        source_execution_duration=random.uniform(0, 100),
    )
    expected_string = "Statue finished successfully after 14.15 seconds!"

    return evaluation, expected_string


def case_success_one_source_two_commands():
    total_execution_duration = 9.31
    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[Path(SOURCE1)] = SourceEvaluation(
        commands_evaluations=[
            CommandEvaluation(
                command=command_mock(COMMAND1),
                success=True,
                execution_duration=random.uniform(0, 100),
            ),
            CommandEvaluation(
                command=command_mock(COMMAND2),
                success=True,
                execution_duration=random.uniform(0, 100),
            ),
        ],
        source_execution_duration=random.uniform(0, 100),
    )
    expected_string = "Statue finished successfully after 9.31 seconds!"

    return evaluation, expected_string


def case_one_source_one_failed_command():
    total_execution_duration = 9.31
    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[Path(SOURCE1)] = SourceEvaluation(
        commands_evaluations=[
            CommandEvaluation(
                command=command_mock(COMMAND1),
                success=False,
                execution_duration=random.uniform(0, 100),
            ),
            CommandEvaluation(
                command=command_mock(COMMAND2),
                success=True,
                execution_duration=random.uniform(0, 100),
            ),
        ],
        source_execution_duration=random.uniform(0, 100),
    )
    expected_string = (
        "Statue has failed after 9.31 seconds on the following commands:\n"
        f"{SOURCE1}:\n"
        f"\t{COMMAND1}\n"
    )

    return evaluation, expected_string


def case_one_source_two_failed_commands():
    total_execution_duration = 9.31
    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[Path(SOURCE1)] = SourceEvaluation(
        commands_evaluations=[
            CommandEvaluation(
                command=command_mock(COMMAND1),
                success=False,
                execution_duration=random.uniform(0, 100),
            ),
            CommandEvaluation(
                command=command_mock(COMMAND2),
                success=False,
                execution_duration=random.uniform(0, 100),
            ),
        ],
        source_execution_duration=random.uniform(0, 100),
    )
    expected_string = (
        "Statue has failed after 9.31 seconds on the following commands:\n"
        f"{SOURCE1}:\n"
        f"\t{COMMAND1}, {COMMAND2}\n"
    )

    return evaluation, expected_string


def case_fail_multiple_sources():
    total_execution_duration = 9.31
    evaluation = Evaluation(total_execution_duration=total_execution_duration)
    evaluation[Path(SOURCE1)] = SourceEvaluation(
        commands_evaluations=[
            CommandEvaluation(
                command=command_mock(COMMAND1),
                success=False,
                execution_duration=random.uniform(0, 100),
            ),
            CommandEvaluation(
                command=command_mock(COMMAND2),
                success=False,
                execution_duration=random.uniform(0, 100),
            ),
        ],
        source_execution_duration=random.uniform(0, 100),
    )
    evaluation[Path(SOURCE2)] = SourceEvaluation(
        commands_evaluations=[
            CommandEvaluation(
                command=command_mock(COMMAND3),
                success=True,
                execution_duration=random.uniform(0, 100),
            )
        ],
        source_execution_duration=random.uniform(0, 100),
    )
    evaluation[Path(SOURCE3)] = SourceEvaluation(
        commands_evaluations=[
            CommandEvaluation(
                command=command_mock(COMMAND4),
                success=False,
                execution_duration=random.uniform(0, 100),
            )
        ],
        source_execution_duration=random.uniform(0, 100),
    )
    evaluation[Path(SOURCE4)] = SourceEvaluation(
        commands_evaluations=[
            CommandEvaluation(
                command=command_mock(COMMAND1),
                success=False,
                execution_duration=random.uniform(0, 100),
            ),
            CommandEvaluation(
                command=command_mock(COMMAND5),
                success=False,
                execution_duration=random.uniform(0, 100),
            ),
        ],
        source_execution_duration=random.uniform(0, 100),
    )
    expected_string = (
        "Statue has failed after 9.31 seconds on the following commands:\n"
        f"{SOURCE1}:\n"
        f"\t{COMMAND1}, {COMMAND2}\n"
        f"{SOURCE3}:\n"
        f"\t{COMMAND4}\n"
        f"{SOURCE4}:\n"
        f"\t{COMMAND1}, {COMMAND5}\n"
    )

    return evaluation, expected_string


@parametrize_with_cases(argnames=["evaluation", "expected_string"], cases=THIS_MODULE)
def test_evaluation_summary_string(evaluation, expected_string):
    actual_result = evaluation_summary_string(evaluation)

    assert click.unstyle(actual_result) == expected_string
