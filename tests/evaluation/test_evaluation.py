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
    failure_map = {}
    commands_map = {}
    return evaluation, failure_map, commands_map


@case(tags=[SUCCESSFUL_TAG])
def case_all_successful():
    evaluation = Evaluation(
        {
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(command=COMMAND1, success=True),
                    CommandEvaluation(command=COMMAND2, success=True),
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(command=COMMAND3, success=True),
                    CommandEvaluation(command=COMMAND4, success=True),
                    CommandEvaluation(command=COMMAND5, success=True),
                ]
            ),
        }
    )
    failure_map = {}
    commands_map = {
        SOURCE1: [COMMAND1, COMMAND2],
        SOURCE2: [COMMAND3, COMMAND4, COMMAND5],
    }
    return evaluation, failure_map, commands_map


@case(tags=[FAILED_TAG])
def case_one_failure():
    evaluation = Evaluation(
        {
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(command=COMMAND1, success=True),
                    CommandEvaluation(command=COMMAND2, success=False),
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(command=COMMAND3, success=True),
                    CommandEvaluation(command=COMMAND4, success=True),
                    CommandEvaluation(command=COMMAND5, success=True),
                ]
            ),
        }
    )
    failure_map = {SOURCE1: [COMMAND2]}
    commands_map = {
        SOURCE1: [COMMAND1, COMMAND2],
        SOURCE2: [COMMAND3, COMMAND4, COMMAND5],
    }
    return evaluation, failure_map, commands_map


@case(tags=[FAILED_TAG])
def case_one_source_with_two_failures():
    evaluation = Evaluation(
        {
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(command=COMMAND1, success=True),
                    CommandEvaluation(command=COMMAND2, success=True),
                    CommandEvaluation(command=COMMAND3, success=True),
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(command=COMMAND4, success=False),
                    CommandEvaluation(command=COMMAND5, success=True),
                    CommandEvaluation(command=COMMAND6, success=False),
                ]
            ),
        }
    )
    failure_map = {SOURCE2: [COMMAND4, COMMAND6]}
    commands_map = {
        SOURCE1: [COMMAND1, COMMAND2, COMMAND3],
        SOURCE2: [COMMAND4, COMMAND5, COMMAND6],
    }
    return evaluation, failure_map, commands_map


@case(tags=[FAILED_TAG])
def case_two_sources_with_failures():
    evaluation = Evaluation(
        {
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(command=COMMAND1, success=False),
                    CommandEvaluation(command=COMMAND2, success=True),
                    CommandEvaluation(command=COMMAND3, success=False),
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(command=COMMAND4, success=True),
                    CommandEvaluation(command=COMMAND5, success=False),
                    CommandEvaluation(command=COMMAND6, success=True),
                ]
            ),
        }
    )
    failure_map = {
        SOURCE1: [COMMAND1, COMMAND3],
        SOURCE2: [COMMAND5],
    }
    commands_map = {
        SOURCE1: [COMMAND1, COMMAND2, COMMAND3],
        SOURCE2: [COMMAND4, COMMAND5, COMMAND6],
    }
    return evaluation, failure_map, commands_map


@parametrize_with_cases(
    argnames=["evaluation", "failure_map", "commands_map"], cases=THIS_MODULE
)
def test_get_commands_map(evaluation, failure_map, commands_map):
    assert failure_map == evaluation.failure_map


@parametrize_with_cases(
    argnames=["evaluation", "failure_map", "commands_map"], cases=THIS_MODULE
)
def test_get_failure_map(evaluation, failure_map, commands_map):
    assert commands_map == evaluation.commands_map


@parametrize_with_cases(
    argnames=["evaluation", "failure_map", "commands_map"],
    cases=THIS_MODULE,
    has_tag=SUCCESSFUL_TAG,
)
def test_evaluation_success(evaluation, failure_map, commands_map):
    assert evaluation.success, "Evaluation should be successful, but it wasn't"


@parametrize_with_cases(
    argnames=["evaluation", "failure_map", "commands_map"],
    cases=THIS_MODULE,
    has_tag=FAILED_TAG,
)
def test_evaluation_failed(evaluation, failure_map, commands_map):
    assert not evaluation.success, "Evaluation should not be successful, but it was"


@parametrize_with_cases(
    argnames=["evaluation", "failure_map", "commands_map"], cases=THIS_MODULE
)
def test_total_commands_count(evaluation, failure_map, commands_map):
    expected_failed_count = sum(
        [len(commands_list) for commands_list in failure_map.values()]
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
    argnames=["evaluation", "failure_map", "commands_map"], cases=THIS_MODULE
)
def test_source_successful_and_failed_commands_count(
    evaluation, failure_map, commands_map
):
    for source in evaluation.keys():
        source_evaluation = evaluation[source]
        source_failed_commands_number = len(failure_map.get(source, []))
        source_all_commands_number = len(source_evaluation.commands_evaluations)
        assert source_evaluation.commands_number == source_all_commands_number
        assert source_evaluation.failed_commands_number == source_failed_commands_number
        successful_commands = source_all_commands_number - source_failed_commands_number
        assert source_evaluation.successful_commands_number == successful_commands
