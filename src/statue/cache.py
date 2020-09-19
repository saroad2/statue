from pathlib import Path


class Cache:
    @classmethod
    def cache_dir(cls):
        dir_path = Path.cwd() / ".statue"
        if not dir_path.exists():
            dir_path.mkdir()
        return dir_path

    @classmethod
    def cache_file(cls, file_name):
        return cls.cache_dir() / file_name

    @classmethod
    def last_evaluation_path(cls):
        return cls.cache_file("evaluation.json")
