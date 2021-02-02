"""Module for cache related methods."""
import time
from pathlib import Path
from typing import List

from statue.constants import HISTORY_SIZE
from statue.evaluation import Evaluation


class Cache:
    """Cache singleton."""

    @classmethod
    def cache_dir(cls) -> Path:
        """
        Directory of cache files. Created if missing.

        :return: Location path of the cache directory
        :rtype: Path
        """
        return cls.__ensure_dir_exists(Path.cwd() / ".statue")

    @classmethod
    def evaluations_dir(cls) -> Path:
        """
        Directory of cache files. Created if missing.

        :return: Location path of the previous evaluations cache directory
        :rtype: Path
        """
        return cls.__ensure_dir_exists(cls.cache_dir() / "evaluations")

    @classmethod
    def all_evaluation_paths(cls) -> List[Path]:
        """
        Get all evaluation paths, ordered from recent to last.

        :return: List of all previous evaluations paths
        :rtype: List[Path]
        """
        evaluations_files = list(cls.evaluations_dir().iterdir())
        evaluations_files.sort(key=cls.__extract_time_stamp, reverse=True)
        return evaluations_files

    @classmethod
    def evaluation_path(cls, n: int):  # pylint: disable=invalid-name
        """
        Get the nth most recent evaluation result path.

        :param n: Evaluation index
        :type n: int
        :return: Evaluation path of the nth evalaution
        :rtype: Path
        """
        evaluations_files = cls.all_evaluation_paths()
        if n >= len(evaluations_files):
            return None
        return evaluations_files[n]

    @classmethod
    def recent_evaluation_path(cls) -> Path:
        """
        Get last evaluation result path.

        :return: Most recent evaluation path
        :rtype: Path
        """
        return cls.evaluation_path(0)

    @classmethod
    def save_evaluation(cls, evaluation: Evaluation):
        """
        Save evaluation to cache.

        Deletes old evaluations after saving according to history size.

        :param evaluation: Evaluation instance to be saved
        :type evaluation: Evaluation
        """
        file_name = f"evaluation-{int(time.time())}.json"
        evaluation.save_as_json(cls.evaluations_dir() / file_name)
        cls.__remove_old_evaluations()

    @classmethod
    def __extract_time_stamp(cls, path: Path):
        return int(path.stem.split("-")[-1])

    @classmethod
    def __ensure_dir_exists(cls, dir_path: Path) -> Path:
        dir_path.mkdir(exist_ok=True)
        return dir_path

    @classmethod
    def __remove_old_evaluations(cls):
        evaluation_files = cls.all_evaluation_paths()
        if len(evaluation_files) <= HISTORY_SIZE:
            return
        for evaluation_file in evaluation_files[HISTORY_SIZE:]:
            evaluation_file.unlink()
