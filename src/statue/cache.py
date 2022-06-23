"""Module for cache related methods."""
from collections import deque
from pathlib import Path
from typing import Deque, List, Optional, Sequence, Set

from statue.evaluation import Evaluation
from statue.exceptions import CacheError


class Cache:
    """Cache files repository."""

    def __init__(
        self,
        size: int,
        cache_root_directory: Optional[Path] = None,
        enabled: bool = True,
    ):
        """
        Initialize cache.

        :param size: Number of evaluations to save
        :type size: int
        :param cache_root_directory: Optional root directory for caching
        :type cache_root_directory: Optional[Path]
        :param enabled: Whether caching is enabled or not. True by default.
        :type enabled: bool
        """
        self._all_evaluations: Deque[Evaluation] = deque()
        self.cache_root_directory = cache_root_directory
        self.history_size = size
        self.enabled = enabled

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
        if cache_dir is None:
            return
        self.__ensure_dir_exists(cache_dir)
        self.load_evaluations()

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
    def all_evaluation_paths(self) -> Set[Path]:
        """
        Get all evaluation paths, ordered from recent to last.

        :return: Set of all previous evaluations paths
        :rtype: Set[Path]
        """
        if self.evaluations_dir is None:
            return set()
        return set(self.evaluations_dir.iterdir())

    @property
    def all_evaluations(self) -> List[Evaluation]:
        """All cached evaluations."""
        return list(self._all_evaluations)

    @all_evaluations.setter
    def all_evaluations(self, evaluations: Sequence[Evaluation]):
        self.all_evaluations.clear()
        evaluations = list(evaluations)
        evaluations.sort(key=lambda evaluation: evaluation.timestamp)
        self._all_evaluations.extendleft(evaluations)

    @property
    def number_of_evaluations(self) -> int:
        """Get number of cached evaluations."""
        return len(self.all_evaluations)

    @property
    def recent_failed_evaluation(self) -> Evaluation:
        """Get the most recent failed evaluation."""
        for evaluation in self.all_evaluations:
            if not evaluation.success:
                return evaluation
        raise CacheError("Could not find failed evaluation")

    def get_evaluation(self, n: int) -> Evaluation:
        """
        Get the nth most recent evaluation.

        :param n: Evaluation index
        :type n: int
        :return: The nth evaluation
        :rtype: Evaluation
        :raises CacheError: raised when receiving an invalid index for evaluation
        """
        if n < 0 or n >= self.number_of_evaluations:
            raise CacheError(
                "Could not get the desired evaluation due to invalid index"
            )
        return self.all_evaluations[n]

    def save_evaluation(self, evaluation: Evaluation):
        """
        Save evaluation to cache.

        Deletes old evaluations after saving according to history size.

        :param evaluation: Evaluation instance to be saved
        :type evaluation: Evaluation
        """
        self._all_evaluations.appendleft(evaluation)
        evaluation.save_as_json(self.__get_evaluation_path(evaluation))
        while len(self.all_evaluations) > self.history_size:
            self.__remove_oldest_evaluation()

    def clear(self, limit: Optional[int] = None):
        """
        Remove evaluations from cache.

        :param limit: Optional. limit the number of evaluations to be deleted
        :type limit: Optional[int]
        """
        number_of_evaluations_to_be_deleted = (
            limit if limit is not None else self.number_of_evaluations
        )
        for _ in range(number_of_evaluations_to_be_deleted):
            self.__remove_oldest_evaluation()

    def load_evaluations(self):
        """Load all evaluations from evaluations directory."""
        self.all_evaluations = [
            Evaluation.load_from_file(evaluation_path)
            for evaluation_path in self.all_evaluation_paths
        ]

    def __remove_oldest_evaluation(self):
        evaluation = self._all_evaluations.pop()
        self.__get_evaluation_path(evaluation).unlink()

    def __get_evaluation_path(self, evaluation: Evaluation) -> Path:
        if self.evaluations_dir is None:
            raise CacheError("Cache directory was not specified")
        seconds_since_epoch = int(evaluation.timestamp.timestamp())
        return self.evaluations_dir / f"evaluation-{seconds_since_epoch}.json"

    @classmethod
    def __ensure_dir_exists(cls, dir_path: Path) -> Path:
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
