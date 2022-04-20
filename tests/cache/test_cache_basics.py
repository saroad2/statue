import random

import mock
import pytest
from pytest_cases import parametrize

from statue.cache import Cache
from tests.util import dummy_time_stamps, successful_evaluation_mock


def test_cache_constructor_with_none_root_directory(tmp_path):
    size = random.randint(1, 100)
    cache = Cache(size=size)
    assert cache.cache_root_directory is None
    assert cache.evaluations_dir is None
    assert not cache.all_evaluation_paths
    assert cache.history_size == size
    assert cache.number_of_evaluations == 0


def test_cache_constructor_with_non_existing_directory(tmp_path):
    cache_dir = tmp_path / "cache"
    assert not cache_dir.exists()

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)
    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert not cache.all_evaluation_paths
    assert cache.history_size == size
    assert cache.number_of_evaluations == 0


def test_cache_constructor_with_existing_directory(tmp_path):
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert not cache.all_evaluation_paths
    assert cache.history_size == size
    assert cache.number_of_evaluations == 0


def test_cache_constructor_with_evaluations_directory_already_existing(tmp_path):
    cache_dir = tmp_path / "cache"
    (cache_dir / "evaluations").mkdir(parents=True)

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert not cache.all_evaluation_paths
    assert cache.history_size == size
    assert cache.number_of_evaluations == 0


def test_cache_constructor_with_existing_evaluations(
    tmp_path, mock_evaluation_load_from_file
):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [evaluations_dir / f"evaluation_{i}.json" for i in range(6)]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()
    evaluations = [
        successful_evaluation_mock(timestamp=time_stamp)
        for time_stamp in dummy_time_stamps(len(evaluation_paths), reverse=True)
    ]
    mock_evaluation_load_from_file.side_effect = dict(
        zip(evaluation_paths, evaluations)
    ).get

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert cache.history_size == size
    assert cache.number_of_evaluations == len(evaluation_paths)
    assert cache.all_evaluation_paths == set(evaluation_paths)
    assert cache.all_evaluations == evaluations

    assert mock_evaluation_load_from_file.call_count == len(evaluation_paths)
    mock_evaluation_load_from_file.assert_has_calls(
        [mock.call(evaluation_path) for evaluation_path in evaluation_paths],
        any_order=True,
    )


@pytest.mark.parametrize(argnames="evaluation_index", argvalues=range(6))
def test_cache_get_evaluation(
    tmp_path, evaluation_index, mock_evaluation_load_from_file
):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [evaluations_dir / f"evaluation_{i}.json" for i in range(6)]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()
    evaluations = [
        successful_evaluation_mock(timestamp=time_stamp)
        for time_stamp in dummy_time_stamps(len(evaluation_paths), reverse=True)
    ]
    mock_evaluation_load_from_file.side_effect = dict(
        zip(evaluation_paths, evaluations)
    ).get

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert cache.get_evaluation(evaluation_index) == evaluations[evaluation_index]


def test_cache_clear(tmp_path, mock_evaluation_load_from_file):
    time_stamps = dummy_time_stamps(5)
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / f"evaluation-{int(timestamp.timestamp())}.json"
        for timestamp in time_stamps
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()
    evaluations = [
        successful_evaluation_mock(timestamp=time_stamp) for time_stamp in time_stamps
    ]
    mock_evaluation_load_from_file.side_effect = dict(
        zip(evaluation_paths, evaluations)
    ).get

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)
    cache.clear()

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert not cache.all_evaluation_paths
    assert cache.history_size == size
    assert cache.number_of_evaluations == 0

    for evaluation_file in evaluation_paths:
        assert not evaluation_file.exists()


def test_cache_clear_with_limit(tmp_path, mock_evaluation_load_from_file):
    number_of_evaluations = 6
    limit = 4
    time_stamps = dummy_time_stamps(number_of_evaluations)

    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / f"evaluation-{int(timestamp.timestamp())}.json"
        for timestamp in time_stamps
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()
    evaluations = [
        successful_evaluation_mock(timestamp=time_stamp) for time_stamp in time_stamps
    ]
    mock_evaluation_load_from_file.side_effect = dict(
        zip(evaluation_paths, evaluations)
    ).get

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)
    cache.clear(limit=limit)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert cache.all_evaluation_paths == set(evaluation_paths[limit:])
    assert cache.history_size == size
    assert cache.number_of_evaluations == len(evaluation_paths) - limit

    for evaluation_file in evaluation_paths[:limit]:
        assert not evaluation_file.exists()
    for evaluation_file in evaluation_paths[limit:]:
        assert evaluation_file.exists()


def test_cache_constructor_with_history_size(tmp_path):
    history_size = 8
    cache = Cache(size=history_size)
    assert cache.cache_root_directory is None
    assert cache.evaluations_dir is None
    assert not cache.all_evaluation_paths
    assert cache.history_size == history_size


@parametrize(argnames="invalid_evaluation_index", argvalues=[-1, 10])
def test_cache_get_evaluation_with_invalid_index(
    tmp_path, mock_evaluation_load_from_file, invalid_evaluation_index
):
    number_of_evaluations = 6
    time_stamps = dummy_time_stamps(number_of_evaluations)
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / f"evaluation-{i}.json" for i in range(number_of_evaluations)
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()
    evaluations = [
        successful_evaluation_mock(timestamp=time_stamp) for time_stamp in time_stamps
    ]
    mock_evaluation_load_from_file.side_effect = dict(
        zip(evaluation_paths, evaluations)
    ).get

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    with pytest.raises(
        IndexError, match="^Could not get the desired evaluation due to invalid index$"
    ):
        cache.get_evaluation(invalid_evaluation_index)
