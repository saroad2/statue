from pytest_cases import parametrize_with_cases, THIS_MODULE

from statue.evaluation import (
    Evaluation,
    get_failure_map,
    SourceEvaluation,
    CommandEvaluation,
)
from tests.constants import (
    SOURCE1,
    SOURCE2,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
)


def case_empty():
    evaluation = Evaluation()
    failure_map = {}
    return evaluation, failure_map


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
    return evaluation, failure_map


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
    return evaluation, failure_map


def case_one_source_with_two_failures():
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
                    CommandEvaluation(command=COMMAND3, success=False),
                    CommandEvaluation(command=COMMAND4, success=True),
                    CommandEvaluation(command=COMMAND5, success=False),
                ]
            ),
        }
    )
    failure_map = {SOURCE2: [COMMAND3, COMMAND5]}
    return evaluation, failure_map


def case_two_sources_with_failures():
    evaluation = Evaluation(
        {
            SOURCE1: SourceEvaluation(
                [
                    CommandEvaluation(command=COMMAND1, success=False),
                    CommandEvaluation(command=COMMAND2, success=True),
                ]
            ),
            SOURCE2: SourceEvaluation(
                [
                    CommandEvaluation(command=COMMAND3, success=False),
                    CommandEvaluation(command=COMMAND4, success=True),
                    CommandEvaluation(command=COMMAND5, success=False),
                ]
            ),
        }
    )
    failure_map = {
        SOURCE1: [COMMAND1],
        SOURCE2: [COMMAND3, COMMAND5],
    }
    return evaluation, failure_map


@parametrize_with_cases(argnames=["evaluation", "failure_map"], cases=THIS_MODULE)
def test_get_failure_map(evaluation, failure_map):
    assert failure_map == get_failure_map(evaluation)
