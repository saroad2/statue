from pathlib import Path
from typing import List

from git import Repo
from pytest_cases import THIS_MODULE, fixture, parametrize_with_cases

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


@fixture
def path_tmpdir(tmpdir):
    return Path(tmpdir)


def case_non_python_file(path_tmpdir):
    return None, existing_file(path_tmpdir, "bla.txt"), []


def case_python_file(path_tmpdir):
    python_file = existing_file(path_tmpdir, "bla.py")
    return None, python_file, [python_file]


def case_empty_directory(path_tmpdir):
    return None, path_tmpdir, []


def case_directory_with_one_python_file(path_tmpdir):
    one = existing_file(path_tmpdir, "one.py")
    existing_files(path_tmpdir, file_names=["two.txt", "three.txt", "four.txt"])
    return None, path_tmpdir, [one]


def case_directory_with_two_python_file(path_tmpdir):
    python_files = existing_files(path_tmpdir, file_names=["one.py", "two.py"])
    existing_files(path_tmpdir, file_names=["three.txt", "four.txt"])
    return None, path_tmpdir, python_files


def case_one_python_file_from_inner_directory(path_tmpdir):
    one = existing_file(path_tmpdir, "inner", "one.py")
    return None, path_tmpdir, [one]


def case_two_python_files_from_inner_directory(path_tmpdir):
    python_files = existing_files(path_tmpdir, "inner", file_names=["one.py", "two.py"])
    return None, path_tmpdir, python_files


def case_ignore_one_python_file(path_tmpdir):
    one = existing_file(path_tmpdir, "one.py")
    two = existing_file(path_tmpdir, "two.py")
    existing_files(path_tmpdir, file_names=["three.txt", "four.txt"])
    repo = Repo.init(path_tmpdir)
    ignore_paths(repo=repo, files=[two])
    return repo, path_tmpdir, [one]


def case_ignore_inner_directory(path_tmpdir):
    inner = path_tmpdir / "inner"
    existing_files(inner, file_names=["one.py", "two.py"])
    repo = Repo.init(path_tmpdir)
    ignore_paths(repo, files=[inner])
    return repo, path_tmpdir, []


@parametrize_with_cases(argnames=["repo", "directory", "sources"], cases=THIS_MODULE)
def test_sources_finder(repo, directory, sources):
    assert find_sources(directory, repo=repo) == sources
