"""Module for cache related methods."""
from pathlib import Path


class Cache:
    """Cache singleton."""

    @classmethod
    def cache_dir(cls) -> Path:
        """Directory of cache files. Created if missing."""
        dir_path = Path.cwd() / ".statue"
        if not dir_path.exists():
            dir_path.mkdir()
        return dir_path

    @classmethod
    def cache_file(cls, file_name: str) -> Path:
        """Get a cache file by name."""
        return cls.cache_dir() / file_name

    @classmethod
    def last_evaluation_path(cls) -> Path:
        """Get last evaluation result path."""
        return cls.cache_file("evaluation.json")
