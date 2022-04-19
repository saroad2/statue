import random

import mock
import pytest

from statue.cache import Cache

EVALUATION_PATH_NAMES = [
    "evaluation-1000.json",
    "evaluation-999.json",
    "evaluation-900.json",
    "evaluation-889.json",
    "evaluation-700.json",
    "evaluation-88.json",
    "evaluation-70.json",
]


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


def test_cache_constructor_with_existing_evaluations(tmp_path):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / evaluation_path_name
        for evaluation_path_name in EVALUATION_PATH_NAMES
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert cache.history_size == size
    assert cache.number_of_evaluations == len(evaluation_paths)


def test_cache_all_evaluation_paths(tmp_path):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / evaluation_path_name
        for evaluation_path_name in EVALUATION_PATH_NAMES
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert cache.all_evaluation_paths == evaluation_paths


def test_cache_all_evaluations(tmp_path, mock_evaluation_load_from_file):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / evaluation_path_name
        for evaluation_path_name in EVALUATION_PATH_NAMES
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()
    evaluations = [mock.Mock() for _ in range(len(evaluation_paths))]
    mock_evaluation_load_from_file.side_effect = evaluations

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert cache.all_evaluations == evaluations
    assert mock_evaluation_load_from_file.call_count == len(evaluation_paths)
    assert mock_evaluation_load_from_file.call_args_list == [
        mock.call(evaluation_path) for evaluation_path in evaluation_paths
    ]


@pytest.mark.parametrize(
    argnames="evaluation_index", argvalues=range(len(EVALUATION_PATH_NAMES))
)
def test_cache_get_evaluation_path(tmp_path, evaluation_index):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / evaluation_path_name
        for evaluation_path_name in EVALUATION_PATH_NAMES
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert cache.evaluation_path(evaluation_index) == evaluation_paths[evaluation_index]


@pytest.mark.parametrize(
    argnames="evaluation_index", argvalues=range(len(EVALUATION_PATH_NAMES))
)
def test_cache_get_evaluation(
    tmp_path, evaluation_index, mock_evaluation_load_from_file
):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / evaluation_path_name
        for evaluation_path_name in EVALUATION_PATH_NAMES
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert (
        cache.get_evaluation(evaluation_index)
        == mock_evaluation_load_from_file.return_value
    )
    mock_evaluation_load_from_file.assert_called_once_with(
        evaluation_paths[evaluation_index]
    )


def test_cache_clear(tmp_path):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / evaluation_path_name
        for evaluation_path_name in EVALUATION_PATH_NAMES
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()

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


def test_cache_clear_with_limit(tmp_path):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_paths = [
        evaluations_dir / evaluation_path_name
        for evaluation_path_name in EVALUATION_PATH_NAMES
    ]
    for evaluation_file in evaluation_paths:
        evaluation_file.touch()
    limit = len(evaluation_paths) // 2

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)
    cache.clear(limit=limit)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert cache.all_evaluation_paths == evaluation_paths[:-limit]
    assert cache.history_size == size
    assert cache.number_of_evaluations == len(evaluation_paths) - limit

    for evaluation_file in evaluation_paths[:-limit]:
        assert evaluation_file.exists()
    for evaluation_file in evaluation_paths[-limit:]:
        assert not evaluation_file.exists()


def test_cache_constructor_with_history_size(tmp_path):
    history_size = 8
    cache = Cache(size=history_size)
    assert cache.cache_root_directory is None
    assert cache.evaluations_dir is None
    assert not cache.all_evaluation_paths
    assert cache.history_size == history_size
