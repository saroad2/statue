import datetime
import random
from unittest import mock

import pytest
from pytest_cases import parametrize

from statue.cache import Cache
from statue.exceptions import CacheError
from tests.util import successful_evaluation_mock


def test_save_evaluation(tmp_path, mock_evaluation_load_from_file):
    timestamp = 12300566
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_path = evaluations_dir / f"evaluation-{timestamp}.json"

    evaluation = mock.Mock()
    evaluation.timestamp = datetime.datetime.fromtimestamp(timestamp)
    evaluation.save_as_json.side_effect = lambda path: path.touch()
    mock_evaluation_load_from_file.return_value = evaluation

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert not evaluation_path.exists()

    cache.save_evaluation(evaluation)

    evaluation.save_as_json.assert_called_with(evaluation_path)
    mock_evaluation_load_from_file.assert_called_once_with(evaluation_path)
    assert evaluation_path.exists()


def test_save_evaluation_deletes_old_evaluations(  # pylint: disable=too-many-locals
    tmp_path, mock_evaluation_load_from_file
):
    size = random.randint(1, 100)
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)

    now_timestmamp = int(datetime.datetime.now().replace(microsecond=0).timestamp())
    time_stamps = [
        now_timestmamp + delta
        for delta in random.sample(range(1, 1_000_000), k=size + 1)
    ]
    time_stamps.sort(reverse=True)
    old_time_stamps, recent_time_stamp = time_stamps[1:], time_stamps[0]
    old_evaluation_paths = [
        evaluations_dir / f"evaluation-{time_stamp}.json"
        for time_stamp in old_time_stamps
    ]
    for old_evaluation_file in old_evaluation_paths:
        old_evaluation_file.touch()
    recent_evaluation_file = evaluations_dir / f"evaluation-{recent_time_stamp}.json"

    recent_evaluation = successful_evaluation_mock(
        timestamp=datetime.datetime.fromtimestamp(recent_time_stamp)
    )
    old_evaluations = [
        successful_evaluation_mock(timestamp=datetime.datetime.fromtimestamp(timestamp))
        for timestamp in old_time_stamps
    ]
    recent_evaluation.save_as_json.side_effect = lambda path: path.touch()
    mock_evaluation_load_from_file.side_effect = [recent_evaluation] + old_evaluations

    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert not recent_evaluation_file.exists()

    cache.save_evaluation(recent_evaluation)

    assert recent_evaluation_file.exists()
    recent_evaluation.save_as_json.assert_called_with(recent_evaluation_file)
    for i, old_evaluation_file in enumerate(old_evaluation_paths[:-1]):
        assert old_evaluation_file.exists(), f"The {i}th old file does not exist."
    assert not old_evaluation_paths[-1].exists()


def test_cache_save_evaluation_fails_when_no_root_dir_was_set():
    size = random.randint(1, 100)
    cache = Cache(size=size)
    evaluation = mock.Mock()

    with pytest.raises(CacheError, match="^Cache directory was not specified$"):
        cache.save_evaluation(evaluation)


@parametrize(argnames="invalid_evaluation_index", argvalues=[-1, 10])
def test_cache_get_evaluation_with_invalid_index(tmp_path, invalid_evaluation_index):
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

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    with pytest.raises(
        IndexError, match="^Could not get the desired evaluation due to invalid index$"
    ):
        cache.evaluation_path(invalid_evaluation_index)
