from statue.cache import Cache
from statue.constants import DEFAULT_HISTORY_SIZE


def test_cache_constructor_with_none_root_directory(tmp_path):
    cache = Cache()
    assert cache.cache_root_directory is None
    assert cache.evaluations_dir is None
    assert not cache.all_evaluation_paths
    assert cache.history_size == DEFAULT_HISTORY_SIZE


def test_cache_constructor_with_non_existing_directory(tmp_path):
    cache_dir = tmp_path / "cache"
    assert not cache_dir.exists()

    cache = Cache(cache_dir)
    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert not cache.all_evaluation_paths
    assert cache.history_size == DEFAULT_HISTORY_SIZE


def test_cache_constructor_with_existing_directory(tmp_path):
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()

    cache = Cache(cache_dir)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert not cache.all_evaluation_paths
    assert cache.history_size == DEFAULT_HISTORY_SIZE


def test_cache_constructor_with_evaluations_directory_already_existing(tmp_path):
    cache_dir = tmp_path / "cache"
    (cache_dir / "evaluations").mkdir(parents=True)

    cache = Cache(cache_dir)

    assert cache.cache_root_directory == cache_dir
    assert cache_dir.exists()
    assert cache.evaluations_dir == cache_dir / "evaluations"
    assert cache.evaluations_dir.exists()
    assert not cache.all_evaluation_paths
    assert cache.history_size == DEFAULT_HISTORY_SIZE


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
    assert cache.history_size == DEFAULT_HISTORY_SIZE


def test_cache_constructor_with_history_size(tmp_path):
    history_size = 8
    cache = Cache(size=history_size)
    assert cache.cache_root_directory is None
    assert cache.evaluations_dir is None
    assert not cache.all_evaluation_paths
    assert cache.history_size == history_size
