from pytest_cases import THIS_MODULE, case, parametrize_with_cases

from statue.evaluation import (
    CommandEvaluation,
    Evaluation,
    SourceEvaluation,
    get_failure_map,
)
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
    COMMAND6,
    SOURCE1,
    SOURCE2,
)

SUCCESSFUL_TAG = "successful"
FAILED_TAG = "failed"


@case(tags=[SUCCESSFUL_TAG])
def case_empty():
    evaluation = Evaluation()
    failure_map = {}
    commands_number = 0
    return evaluation, failure_map, commands_number


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
    commands_number = 5
    return evaluation, failure_map, commands_number


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
    commands_number = 5
    return evaluation, failure_map, commands_number


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
    commands_number = 6
    return evaluation, failure_map, commands_number


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
        SOURCE1: [
            COMMAND1,
            COMMAND3,
        ],
        SOURCE2: [COMMAND5],
    }
    commands_number = 6
    return evaluation, failure_map, commands_number


@parametrize_with_cases(argnames=["evaluation", "failure_map"], cases=THIS_MODULE)
def test_get_failure_map(evaluation, failure_map):
    assert failure_map == get_failure_map(evaluation)


@parametrize_with_cases(
    argnames=["evaluation", "failure_map"], cases=THIS_MODULE, has_tag=SUCCESSFUL_TAG
)
def test_evaluation_success(evaluation, failure_map):
    assert evaluation.success, "Evaluation should be successful, but it wasn't"


@parametrize_with_cases(
    argnames=["evaluation", "failure_map"], cases=THIS_MODULE, has_tag=FAILED_TAG
)
def test_evaluation_failed(evaluation, failure_map):
    assert not evaluation.success, "Evaluation should not be successful, but it was"


@parametrize_with_cases(
    argnames=["evaluation", "failure_map", "commands_number"], cases=THIS_MODULE
)
def test_total_commands_count(evaluation, failure_map, commands_number):
    expected_failed_count = sum(
        [len(commands_list) for commands_list in failure_map.values()]
    )
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
    argnames=["evaluation", "failure_map", "commands_number"], cases=THIS_MODULE
)
def test_source_successful_and_failed_commands_count(
    evaluation, failure_map, commands_number
):
    for source in evaluation.keys():
        source_evaluation = evaluation[source]
        source_failed_commands_number = len(failure_map.get(source, []))
        source_all_commands_number = len(source_evaluation.commands_evaluations)
        assert source_evaluation.commands_number == source_all_commands_number
        assert source_evaluation.failed_commands_number == source_failed_commands_number
        assert (
            source_evaluation.successful_commands_number
            == source_all_commands_number - source_failed_commands_number
        )
