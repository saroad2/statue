"""Find all python sources in a directory."""
from pathlib import Path

from git import Repo


def find_sources(path: Path, repo: Repo = None):
    """Search for sources recursively."""
    if is_python(path):
        return [path]
    if not path.is_dir():
        return []
    return expend(path, repo)


def expend(path, repo=None):
    """Find all sources inside a directory which are not ignored."""
    inner_files = list(path.iterdir())
    if repo is not None:
        ignored_files = [Path(ignored) for ignored in repo.ignored(inner_files)]
        inner_files = [
            inner_path for inner_path in inner_files if inner_path not in ignored_files
        ]
    sources = []
    for inner_path in inner_files:
        sources.extend(find_sources(inner_path, repo=repo))
    return sorted(sources)


def is_python(path: Path) -> bool:
    """Is path a python module or package."""
    return is_python_module(path) or is_python_package(path)


def is_python_module(path: Path) -> bool:
    """Is path a python module."""
    return path.is_file() and path.suffix == ".py"


def is_python_package(path: Path) -> bool:
    """Is path a python package."""
    return path.is_dir() and (path / "__init__.py").exists()
