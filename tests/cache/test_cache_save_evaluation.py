import datetime
import random
from unittest import mock

import pytest

from statue.cache import Cache
from statue.exceptions import CacheError
from tests.util import dummy_time_stamps, successful_evaluation_mock


def test_save_evaluation(tmp_path, mock_evaluation_load_from_file):
    timestamp = 12300566
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)
    evaluation_path = evaluations_dir / f"evaluation-{timestamp}.json"

    evaluation = mock.Mock()
    evaluation.timestamp = datetime.datetime.fromtimestamp(timestamp)
    evaluation.save_as_json.side_effect = lambda path: path.touch()

    size = random.randint(1, 100)
    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert not evaluation_path.exists()

    cache.save_evaluation(evaluation)

    evaluation.save_as_json.assert_called_with(evaluation_path)
    mock_evaluation_load_from_file.assert_not_called()
    assert evaluation_path.exists()


@pytest.mark.parametrize("size", [random.randint(2, 100), 1])
def test_save_evaluation_deletes_old_evaluations(  # pylint: disable=too-many-locals
    tmp_path, mock_evaluation_load_from_file, size
):
    cache_dir = tmp_path / "cache"
    evaluations_dir = cache_dir / "evaluations"
    evaluations_dir.mkdir(parents=True)

    time_stamps = dummy_time_stamps(size + 1)
    old_time_stamps, recent_time_stamp = time_stamps[:-1], time_stamps[-1]
    old_evaluation_paths = [
        evaluations_dir / f"evaluation-{int(time_stamp.timestamp())}.json"
        for time_stamp in old_time_stamps
    ]
    for old_evaluation_file in old_evaluation_paths:
        old_evaluation_file.touch()
    recent_evaluation_path = (
        evaluations_dir / f"evaluation-{int(recent_time_stamp.timestamp())}.json"
    )

    recent_evaluation = successful_evaluation_mock(timestamp=recent_time_stamp)
    old_evaluations = [
        successful_evaluation_mock(timestamp=timestamp) for timestamp in old_time_stamps
    ]
    recent_evaluation.save_as_json.side_effect = lambda path: path.touch()
    evaluation_paths_dict = dict(zip(old_evaluation_paths, old_evaluations))
    evaluation_paths_dict[recent_evaluation_path] = recent_evaluation
    mock_evaluation_load_from_file.side_effect = evaluation_paths_dict.get

    cache = Cache(size=size, cache_root_directory=cache_dir)

    assert not recent_evaluation_path.exists()

    cache.save_evaluation(recent_evaluation)

    assert recent_evaluation_path.exists()
    recent_evaluation.save_as_json.assert_called_with(recent_evaluation_path)
    for i, old_evaluation_file in enumerate(old_evaluation_paths[1:]):
        assert old_evaluation_file.exists(), f"The {i}th old file does not exist."
    assert not old_evaluation_paths[0].exists()


def test_cache_save_evaluation_fails_when_no_root_dir_was_set():
    size = random.randint(1, 100)
    cache = Cache(size=size)
    evaluation = mock.Mock()

    with pytest.raises(CacheError, match="^Cache directory was not specified$"):
        cache.save_evaluation(evaluation)
