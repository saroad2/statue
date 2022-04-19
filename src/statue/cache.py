"""Module for cache related methods."""
from pathlib import Path
from typing import List, Optional

from statue.evaluation import Evaluation
from statue.exceptions import CacheError


class Cache:
    """Cache files repository."""

    def __init__(
        self,
        size: int,
        cache_root_directory: Optional[Path] = None,
    ):
        """
        Initialize cache.

        :param cache_root_directory: Optional root directory for caching
        :type cache_root_directory: Optional[Path]
        :param size: Number of evaluations to save
        :type size: int
        """
        self.cache_root_directory = cache_root_directory
        self.history_size = size

    @property
    def cache_root_directory(self) -> Optional[Path]:
        """Root directory for caching."""
        return self._cache_root_directory

    @cache_root_directory.setter
    def cache_root_directory(self, cache_dir: Optional[Path]):
        """
        Set root directory for caching.

        :param cache_dir: Root directory for caching
        :type cache_dir: Optional[Path]
        """
        self._cache_root_directory = cache_dir
        if cache_dir is not None:
            self.__ensure_dir_exists(cache_dir)

    @property
    def evaluations_dir(self) -> Optional[Path]:
        """
        Directory of cache files. Created if missing.

        :return: Location path of the previous evaluations cache directory
        :rtype: Path
        """
        if self.cache_root_directory is None:
            return None
        return self.__ensure_dir_exists(self.cache_root_directory / "evaluations")

    @property
    def all_evaluation_paths(self) -> List[Path]:
        """
        Get all evaluation paths, ordered from recent to last.

        :return: List of all previous evaluations paths
        :rtype: List[Path]
        """
        if self.evaluations_dir is None:
            return []
        evaluations_files = list(self.evaluations_dir.iterdir())
        evaluations_files.sort(key=self.extract_time_stamp_from_path, reverse=True)
        return evaluations_files

    @property
    def all_evaluations(self) -> List[Evaluation]:
        """All cached evaluations."""
        return [
            Evaluation.load_from_file(evaluation_path)
            for evaluation_path in self.all_evaluation_paths
        ]

    def evaluation_path(self, n: int) -> Path:
        """
        Get the nth most recent evaluation result path.

        :param n: Evaluation index
        :type n: int
        :return: Evaluation path of the nth evaluation
        :rtype: Path
        :raises IndexError: Raised when given index does not match any evaluation
        """
        evaluations_files = self.all_evaluation_paths
        if n < 0 or n >= len(evaluations_files):
            raise IndexError(
                "Could not get the desired evaluation due to invalid index"
            )
        return evaluations_files[n]

    @property
    def number_of_evaluations(self):
        """Get number of cached evaluations."""
        return len(self.all_evaluation_paths)

    def get_evaluation(self, n: int) -> Evaluation:
        """
        Get the nth most recent evaluation.

        :param n: Evaluation index
        :type n: int
        :return: The nth evaluation
        :rtype: Evaluation
        """
        return Evaluation.load_from_file(self.evaluation_path(n))

    def save_evaluation(self, evaluation: Evaluation):
        """
        Save evaluation to cache.

        Deletes old evaluations after saving according to history size.

        :param evaluation: Evaluation instance to be saved
        :type evaluation: Evaluation
        """
        evaluation.save_as_json(self.__get_evaluation_path(evaluation))
        self.__remove_old_evaluations()

    def clear(self, limit: Optional[int] = None):
        """
        Remove evaluations from cache.

        :param limit: Optional. limit the number of evaluations to be deleted
        :type limit: Optional[int]
        """
        evaluation_files_to_be_deleted = self.all_evaluation_paths
        if limit is not None and limit < len(evaluation_files_to_be_deleted):
            # pylint: disable=invalid-unary-operand-type
            evaluation_files_to_be_deleted = evaluation_files_to_be_deleted[-limit:]
        for evaluation_file in evaluation_files_to_be_deleted:
            evaluation_file.unlink()

    @classmethod
    def extract_time_stamp_from_path(cls, evaluation_path: Path) -> int:
        """
        Extract time stamp from an evaluation path.

        :param evaluation_path: Path of saved evaluation.
        :type evaluation_path: Path
        :return: time stamp of the given evaluation
        :rtype: int
        """
        return int(evaluation_path.stem.split("-")[-1])

    def __get_evaluation_path(self, evaluation: Evaluation) -> Path:
        if self.evaluations_dir is None:
            raise CacheError("Cache directory was not specified")
        seconds_since_epoch = int(evaluation.timestamp.timestamp())
        return self.evaluations_dir / f"evaluation-{seconds_since_epoch}.json"

    def __remove_old_evaluations(self):
        evaluations = self.all_evaluations
        if len(evaluations) <= self.history_size:
            return
        for evaluation in evaluations[self.history_size :]:
            self.__remove_evaluation(evaluation)

    def __remove_evaluation(self, evaluation: Evaluation):
        self.__get_evaluation_path(evaluation).unlink()

    @classmethod
    def __ensure_dir_exists(cls, dir_path: Path) -> Path:
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
