import random

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
    assert cache.all_evaluation_paths == evaluation_paths
    assert cache.history_size == size


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


def test_cache_constructor_with_history_size(tmp_path):
    history_size = 8
    cache = Cache(size=history_size)
    assert cache.cache_root_directory is None
    assert cache.evaluations_dir is None
    assert not cache.all_evaluation_paths
    assert cache.history_size == history_size
