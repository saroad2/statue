from pathlib import Path


class Cache:
    @classmethod
    def cache_dir(cls) -> Path:
        dir_path = Path.cwd() / ".statue"
        if not dir_path.exists():
            dir_path.mkdir()
        return dir_path

    @classmethod
    def cache_file(cls, file_name: str) -> Path:
        return cls.cache_dir() / file_name

    @classmethod
    def last_evaluation_path(cls) -> Path:
        return cls.cache_file("evaluation.json")
