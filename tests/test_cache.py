import random
from unittest import mock

import pytest
from pytest_cases import parametrize

from statue.cache import Cache
from statue.constants import DEFAULT_HISTORY_SIZE
from statue.exceptions import CacheError


def test_cache_constructor_with_none_root_directory(tmp_path):
    cache = Cache()
    assert cache.cache_root_directory is None
    assert cache.evaluations_dir is None
    assert not cache.all_evaluation_paths


def test_cache_constructor_with_non_existing_directory(tmp_path):
    cache_dir = tmp_path / "cache"
    assert not cache_dir.exists()

    cache = Cache(cache_dir)
    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert not cache.all_evaluation_paths


def test_cache_constructor_with_existing_directory(tmp_path):
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    cache = Cache(cache_dir)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert not cache.all_evaluation_paths


def test_cache_constructor_with_evaluations_directory_already_existing(tmp_path):
    cache_dir = tmp_path / "cache"
    (cache_dir / "evaluations").mkdir(parents=True)

    cache = Cache(cache_dir)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert not cache.all_evaluation_paths


def test_cache_constructor_with_existing_evaluations(tmp_path):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
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

    cache = Cache(cache_dir)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert cache.all_evaluation_paths == evaluation_paths
    assert cache.recent_evaluation_path == evaluation_paths[0]
    for i, evaluation_path in enumerate(evaluation_paths):
        assert cache.evaluation_path(i) == evaluation_path


def test_save_evaluation(tmp_path, mock_time):
    time = 12300566
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_file = evaluations_dir / f"evaluation-{time}.json"
    mock_time.return_value = time

    evaluation = mock.Mock()
    evaluation.save_as_json.side_effect = lambda path: path.touch()

    cache = Cache(cache_dir)

    assert not evaluation_file.exists()
    cache.save_evaluation(evaluation)
    evaluation.save_as_json.assert_called_with(evaluation_file)
    assert evaluation_file.exists()


def test_save_evaluation_deletes_old_evaluations(tmp_path, mock_time):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)

    time_stamps = list(random.choices(range(1_000_000), k=DEFAULT_HISTORY_SIZE + 1))
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

    cache = Cache(cache_dir)
    cache.save_evaluation(evaluation)
    evaluation.save_as_json.assert_called_with(recent_evaluation_file)

    assert recent_evaluation_file.exists()
    for i, evaluation_file in enumerate(old_evaluations[:-1]):
        assert evaluation_file.exists(), f"The {i}th old file does not exist."
    assert not old_evaluations[-1].exists()


def test_cache_save_evaluation_fails_when_no_root_dir_was_set():
    cache = Cache()
    evaluation = mock.Mock()

    with pytest.raises(CacheError, match="^Cache directory was not specified$"):
        cache.save_evaluation(evaluation)


@parametrize(argnames="invalid_evaluation_index", argvalues=[-1, 10])
def test_cache_get_evaluation_with_invalid_context_(tmp_path, invalid_evaluation_index):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
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

    cache = Cache(cache_dir)

    with pytest.raises(
        IndexError, match="^Could not get the desired evaluation due to invalid index$"
    ):
        cache.evaluation_path(invalid_evaluation_index)
