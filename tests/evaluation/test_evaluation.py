import random

from pytest_cases import THIS_MODULE, case, parametrize_with_cases

from statue.evaluation import CommandEvaluation, Evaluation, SourceEvaluation
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
    COMMAND6,
    FAILED_TAG,
    SOURCE1,
    SOURCE2,
    SUCCESSFUL_TAG,
)


@case(tags=[SUCCESSFUL_TAG])
def case_empty():
    evaluation = Evaluation()
    failure_evaluation = Evaluation()
    commands_map = {}
    return evaluation, failure_evaluation, commands_map


@case(tags=[SUCCESSFUL_TAG])
def case_all_successful():
    evaluation = Evaluation(
        sources_evaluations={
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND1,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND2,
                        execution_duration=random.random(),
                        success=True,
                    ),
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND3,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND4,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND5,
                        execution_duration=random.random(),
                        success=True,
                    ),
                ]
            ),
        }
    )
    failure_evaluation = Evaluation(timestamp=evaluation.timestamp)
    commands_map = {
        SOURCE1: [COMMAND1, COMMAND2],
        SOURCE2: [COMMAND3, COMMAND4, COMMAND5],
    }
    return evaluation, failure_evaluation, commands_map


@case(tags=[FAILED_TAG])
def case_one_failure():
    failed_execution_duration = random.random()
    evaluation = Evaluation(
        sources_evaluations={
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND1,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND2,
                        execution_duration=failed_execution_duration,
                        success=False,
                    ),
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND3,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND4,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND5,
                        execution_duration=random.random(),
                        success=True,
                    ),
                ]
            ),
        }
    )
    failure_evaluation = Evaluation(
        timestamp=evaluation.timestamp,
        sources_evaluations={
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND2,
                        execution_duration=failed_execution_duration,
                        success=False,
                    )
                ]
            )
        },
    )
    commands_map = {
        SOURCE1: [COMMAND1, COMMAND2],
        SOURCE2: [COMMAND3, COMMAND4, COMMAND5],
    }
    return evaluation, failure_evaluation, commands_map


@case(tags=[FAILED_TAG])
def case_one_source_with_two_failures():
    failed_command_duration1, failed_command_duration2 = (
        random.random(),
        random.random(),
    )
    evaluation = Evaluation(
        sources_evaluations={
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND1,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND2,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND3,
                        execution_duration=random.random(),
                        success=True,
                    ),
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND4,
                        execution_duration=failed_command_duration1,
                        success=False,
                    ),
                    CommandEvaluation(
                        command=COMMAND5,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND6,
                        execution_duration=failed_command_duration2,
                        success=False,
                    ),
                ]
            ),
        }
    )
    failure_evaluation = Evaluation(
        timestamp=evaluation.timestamp,
        sources_evaluations={
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND4,
                        execution_duration=failed_command_duration1,
                        success=False,
                    ),
                    CommandEvaluation(
                        command=COMMAND6,
                        execution_duration=failed_command_duration2,
                        success=False,
                    ),
                ]
            )
        },
    )
    commands_map = {
        SOURCE1: [COMMAND1, COMMAND2, COMMAND3],
        SOURCE2: [COMMAND4, COMMAND5, COMMAND6],
    }
    return evaluation, failure_evaluation, commands_map


@case(tags=[FAILED_TAG])
def case_two_sources_with_failures():
    failed_command_duration1, failed_command_duration2, failed_command_duration3 = (
        random.random(),
        random.random(),
        random.random(),
    )
    evaluation = Evaluation(
        sources_evaluations={
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND1,
                        execution_duration=failed_command_duration1,
                        success=False,
                    ),
                    CommandEvaluation(
                        command=COMMAND2,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND3,
                        execution_duration=failed_command_duration2,
                        success=False,
                    ),
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND4,
                        execution_duration=random.random(),
                        success=True,
                    ),
                    CommandEvaluation(
                        command=COMMAND5,
                        execution_duration=failed_command_duration3,
                        success=False,
                    ),
                    CommandEvaluation(
                        command=COMMAND6,
                        execution_duration=random.random(),
                        success=True,
                    ),
                ]
            ),
        }
    )
    failure_evaluation = Evaluation(
        timestamp=evaluation.timestamp,
        sources_evaluations={
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND1,
                        execution_duration=failed_command_duration1,
                        success=False,
                    ),
                    CommandEvaluation(
                        command=COMMAND3,
                        execution_duration=failed_command_duration2,
                        success=False,
                    ),
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(
                        command=COMMAND5,
                        execution_duration=failed_command_duration3,
                        success=False,
                    )
                ]
            ),
        },
    )
    commands_map = {
        SOURCE1: [COMMAND1, COMMAND2, COMMAND3],
        SOURCE2: [COMMAND4, COMMAND5, COMMAND6],
    }
    return evaluation, failure_evaluation, commands_map


@parametrize_with_cases(
    argnames=["evaluation", "failure_evaluation", "commands_map"], cases=THIS_MODULE
)
def test_get_commands_map(evaluation, failure_evaluation, commands_map):
    assert commands_map == evaluation.commands_map


@parametrize_with_cases(
    argnames=["evaluation", "failure_evaluation", "commands_map"], cases=THIS_MODULE
)
def test_get_failure_evaluation(evaluation, failure_evaluation, commands_map):
    assert evaluation.failure_evaluation == failure_evaluation


@parametrize_with_cases(
    argnames=["evaluation", "failure_evaluation", "commands_map"],
    cases=THIS_MODULE,
    has_tag=SUCCESSFUL_TAG,
)
def test_evaluation_success(evaluation, failure_evaluation, commands_map):
    assert evaluation.success, "Evaluation should be successful, but it wasn't"


@parametrize_with_cases(
    argnames=["evaluation", "failure_evaluation", "commands_map"],
    cases=THIS_MODULE,
    has_tag=FAILED_TAG,
)
def test_evaluation_failed(evaluation, failure_evaluation, commands_map):
    assert not evaluation.success, "Evaluation should not be successful, but it was"


@parametrize_with_cases(
    argnames=["evaluation", "failure_evaluation", "commands_map"], cases=THIS_MODULE
)
def test_total_commands_count(evaluation, failure_evaluation, commands_map):
    expected_failed_count = sum(
        [len(commands_list) for commands_list in failure_evaluation.values()]
    )
    commands_number = sum([len(commands) for commands in commands_map.values()])
    expected_successful_count = commands_number - expected_failed_count
    assert (
        evaluation.commands_number == commands_number
    ), "Evaluation commands number is different than expected"
    assert (
        evaluation.failed_commands_number == expected_failed_count
    ), "Evaluation failed commands number is different than expected"
    assert (
        evaluation.successful_commands_number == expected_successful_count
    ), "Evaluation successful commands number is different than expected"


@parametrize_with_cases(
    argnames=["evaluation", "failure_evaluation", "commands_map"], cases=THIS_MODULE
)
def test_source_successful_and_failed_commands_count(
    evaluation, failure_evaluation, commands_map
):
    for source in evaluation.keys():
        source_evaluation = evaluation[source]
        source_failed_commands_number = (
            len(failure_evaluation[source])
            if source in failure_evaluation.keys()
            else 0
        )
        source_all_commands_number = len(source_evaluation.commands_evaluations)
        assert source_evaluation.commands_number == source_all_commands_number
        assert source_evaluation.failed_commands_number == source_failed_commands_number
        successful_commands = source_all_commands_number - source_failed_commands_number
        assert source_evaluation.successful_commands_number == successful_commands
