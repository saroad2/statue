"""Find all python sources in a directory."""
from pathlib import Path
from typing import List

from git import Repo


def find_sources(path: Path, repo: Repo = None) -> List[Path]:
    """
    Search for sources recursively.

    :param path: Path to a dictionary or file
    :type path: Path
    :param repo: Optional. A repository instance. Used to find ignored files
    :type repo: Repo
    :return: List of sources
    :rtype: List[Path]
    """
    if is_python(path):
        return [path]
    if not path.is_dir():
        return []
    return expend(path, repo)


def expend(path: Path, repo: Repo = None) -> List[Path]:
    """
    Find all sources inside a directory which are not ignored.

    :param path: Path to a dictionary or file
    :type path: Path
    :param repo: Optional. A repository instance. Used to find ignored files
    :type repo: Repo
    :return: List of sources
    :rtype: List[Path]
    """
    inner_files = list(path.iterdir())
    if repo is not None:
        ignored_files = [Path(ignored) for ignored in repo.ignored(*inner_files)]
        inner_files = [
            inner_path for inner_path in inner_files if inner_path not in ignored_files
        ]
    sources = []
    for inner_path in inner_files:
        sources.extend(find_sources(inner_path, repo=repo))
    return sorted(sources)


def is_python(path: Path) -> bool:
    """
    Is path a python module or package.

    :param path: Path to a dictionary or file
    :type path: Path
    :return: Is python module or package
    :rtype: bool
    """
    return is_python_module(path) or is_python_package(path)


def is_python_module(path: Path) -> bool:
    """
    Is given path a python module.

    :param path: Path to a dictionary or file
    :type path: Path
    :return: Is python module
    :rtype: bool
    """
    return path.is_file() and path.suffix == ".py"


def is_python_package(path: Path) -> bool:
    """
    Is path a python package.

    :param path: Path to a dictionary or file
    :type path: Path
    :return: Is python package
    :rtype: bool
    """
    return path.is_dir() and (path / "__init__.py").exists()
