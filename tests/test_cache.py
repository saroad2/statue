import random
from unittest import mock

from statue.cache import Cache
from statue.constants import HISTORY_SIZE


def test_create_cache_dir(mock_cwd):
    expected_cache_dir = mock_cwd / ".statue"
    assert not expected_cache_dir.exists()
    assert Cache.cache_dir() == expected_cache_dir
    assert expected_cache_dir.exists()


def test_cache_dir_already_exist(mock_cwd):
    expected_cache_dir = mock_cwd / ".statue"
    expected_cache_dir.mkdir()
    assert Cache.cache_dir() == expected_cache_dir
    assert expected_cache_dir.exists()


def test_create_evaluations_dir(mock_cwd):
    expected_evaluations_dir = mock_cwd / ".statue" / "evaluations"
    assert not expected_evaluations_dir.exists()
    assert Cache.evaluations_dir() == expected_evaluations_dir
    assert expected_evaluations_dir.exists()


def test_evaluations_dir_already_exist(mock_cwd):
    expected_evaluations_dir = mock_cwd / ".statue" / "evaluations"
    expected_evaluations_dir.mkdir(parents=True)
    assert Cache.evaluations_dir() == expected_evaluations_dir
    assert expected_evaluations_dir.exists()


def test_all_evaluations_paths(mock_cwd):
    evaluations_dir = mock_cwd / ".statue" / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / "evaluation-1000.json",
        evaluations_dir / "evaluation-999.json",
        evaluations_dir / "evaluation-900.json",
        evaluations_dir / "evaluation-889.json",
        evaluations_dir / "evaluation-700.json",
        evaluations_dir / "evaluation-88.json",
        evaluations_dir / "evaluation-70.json",
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()
    assert Cache.all_evaluation_paths() == evaluation_paths


def test_numbered_evaluation_path(mock_cwd):
    evaluations_dir = mock_cwd / ".statue" / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / "evaluation-3.json",
        evaluations_dir / "evaluation-2.json",
        evaluations_dir / "evaluation-1.json",
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()
    for i, evaluation_file in enumerate(evaluation_paths):
        assert Cache.evaluation_path(i) == evaluation_file
    assert Cache.evaluation_path(len(evaluation_paths)) is None


def test_recent_evaluation_path(mock_cwd):
    evaluations_dir = mock_cwd / ".statue" / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / "evaluation-3.json",
        evaluations_dir / "evaluation-2.json",
        evaluations_dir / "evaluation-1.json",
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()
    assert Cache.recent_evaluation_path() == evaluation_paths[0]


def test_recent_evaluation_path_when_dir_is_empty(mock_cwd):
    evaluations_dir = mock_cwd / ".statue" / "evaluations"
    evaluations_dir.mkdir(parents=True)
    assert Cache.recent_evaluation_path() is None


def test_save_evaluation(mock_cwd, mock_time):
    time = 12300566
    evaluations_dir = mock_cwd / ".statue" / "evaluations"
    evaluation_file = evaluations_dir / f"evaluation-{time}.json"
    mock_time.return_value = time

    evaluation = mock.Mock()
    evaluation.save_as_json.side_effect = lambda path: path.touch()

    Cache.save_evaluation(evaluation)
    evaluation.save_as_json.assert_called_with(evaluation_file)
    assert evaluation_file.exists()


def test_save_evaluation_deletes_old_evaluations(mock_cwd, mock_time):
    evaluations_dir = mock_cwd / ".statue" / "evaluations"
    evaluations_dir.mkdir(parents=True)

    time_stamps = list(random.choices(range(1_000_000), k=HISTORY_SIZE + 1))
    time_stamps.sort(reverse=True)
    old_time_stamps, recent_time_stamp = time_stamps[1:], time_stamps[0]
    old_evaluations = [
        evaluations_dir / f"evaluation-{time_stamp}.json"
        for time_stamp in old_time_stamps
    ]
    for evaluation_file in old_evaluations:
        evaluation_file.touch()
    recent_evaluation_file = evaluations_dir / f"evaluation-{recent_time_stamp}.json"

    mock_time.return_value = time_stamps[0]
    evaluation = mock.Mock()
    evaluation.save_as_json.side_effect = lambda path: path.touch()

    assert not recent_evaluation_file.exists()

    Cache.save_evaluation(evaluation)
    evaluation.save_as_json.assert_called_with(recent_evaluation_file)

    assert recent_evaluation_file.exists()
    for i, evaluation_file in enumerate(old_evaluations[:-1]):
        assert evaluation_file.exists(), f"The {i}th old file does not exist."
    assert not old_evaluations[-1].exists()
