from pathlib import Path
from typing import List

from git import Repo
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.sources_finder import find_sources


def existing_file(*args):
    directory = Path(*args[:-1])
    directory.mkdir(parents=True, exist_ok=True)
    file_name = args[-1]
    file_obj = directory / file_name
    file_obj.touch()
    return file_obj


def existing_files(*directories, file_names=None):
    directory = Path(*directories)
    return [existing_file(directory, file_name) for file_name in file_names]


def ignore_paths(repo: Repo, files: List[Path]):
    if repo.working_tree_dir is None:
        return
    root_dir = Path(repo.working_tree_dir)
    with open(root_dir / ".gitignore", mode="w", encoding="utf-8") as gitignore:
        for ignored_file in files:
            gitignore.write(str(ignored_file.relative_to(root_dir)))


def case_non_python_file(tmp_path):
    kwargs = {}
    path = existing_file(tmp_path, "bla.txt")
    sources = []
    return kwargs, path, sources


def case_python_file(tmp_path):
    kwargs = {}
    path = existing_file(tmp_path, "bla.py")
    sources = [path]
    return kwargs, path, sources


def case_empty_directory(tmp_path):
    return {}, tmp_path, []


def case_directory_with_one_python_file(tmp_path):
    kwargs = {}
    one = existing_file(tmp_path, "one.py")
    existing_files(tmp_path, file_names=["two.txt", "three.txt", "four.txt"])
    sources = [one]
    return kwargs, tmp_path, sources


def case_directory_with_two_python_file(tmp_path):
    kwargs = {}
    existing_files(tmp_path, file_names=["three.txt", "four.txt"])
    sources = existing_files(tmp_path, file_names=["one.py", "two.py"])
    return kwargs, tmp_path, sources


def case_one_python_file_from_inner_directory(tmp_path):
    kwargs = {}
    one = existing_file(tmp_path, "inner", "one.py")
    sources = [one]
    return kwargs, tmp_path, sources


def case_two_python_files_from_inner_directory(tmp_path):
    kwargs = {}
    sources = existing_files(tmp_path, "inner", file_names=["one.py", "two.py"])
    return kwargs, tmp_path, sources


def case_ignore_one_python_file(tmp_path):
    one = existing_file(tmp_path, "one.py")
    two = existing_file(tmp_path, "two.py")
    existing_files(tmp_path, file_names=["three.txt", "four.txt"])
    repo = Repo.init(tmp_path)
    ignore_paths(repo=repo, files=[two])

    kwargs = dict(repo=repo)
    sources = [one]
    return kwargs, tmp_path, sources


def case_ignore_inner_directory(tmp_path):
    inner = tmp_path / "inner"
    existing_files(inner, file_names=["one.py", "two.py"])
    repo = Repo.init(tmp_path)
    ignore_paths(repo, files=[inner])
    kwargs = dict(repo=repo)
    sources = []
    return kwargs, tmp_path, sources


def case_path_is_excluded(tmp_path):
    tmp_path.touch()
    kwargs = dict(exclude=[tmp_path])
    sources = []
    return kwargs, tmp_path, sources


def case_exclude_one_path(tmp_path):
    path1, path2, path3 = existing_files(
        tmp_path, file_names=["one.py", "two.py", "three.py"]
    )
    kwargs = dict(exclude=[path2])
    sources = [path1, path3]
    return kwargs, tmp_path, sources


def case_exclude_two_paths(tmp_path):
    path1, path2, path3 = existing_files(
        tmp_path, file_names=["one.py", "two.py", "three.py"]
    )
    kwargs = dict(exclude=[path2, path3])
    sources = [path1]
    return kwargs, tmp_path, sources


def case_exclude_directory(tmp_path):
    subdir1, subdir2 = tmp_path / "a", tmp_path / "b"
    existing_files(subdir1, file_names=["one.py", "two.py", "three.py"])
    sources = existing_files(subdir2, file_names=["four.py", "five.py", "six.py"])
    kwargs = dict(exclude=[subdir1])
    return kwargs, tmp_path, sources


def case_exclude_inner_path(tmp_path):
    one, two = existing_files(tmp_path, "a", file_names=["one.py", "two.py"])
    kwargs = dict(exclude=[one])
    sources = [two]
    return kwargs, tmp_path, sources


@parametrize_with_cases(argnames=["kwargs", "path", "sources"], cases=THIS_MODULE)
def test_sources_finder(kwargs, path, sources):
    assert set(find_sources(path, **kwargs)) == set(sources)
