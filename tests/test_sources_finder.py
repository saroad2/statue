from pathlib import Path

from git import Repo
from pytest_cases import parametrize_with_cases, THIS_MODULE, fixture
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


def ignore_paths(repo_root, files):
    Repo.init(repo_root)
    with open(repo_root / ".gitignore", mode="w") as gitignore:
        for ignored_file in files:
            gitignore.write(str(ignored_file.relative_to(repo_root)))


@fixture
def path_tmpdir(tmpdir):
    return Path(tmpdir)


def case_non_python_file(path_tmpdir):
    return existing_file(path_tmpdir, "bla.txt"), []


def case_python_file(path_tmpdir):
    python_file = existing_file(path_tmpdir, "bla.py")
    return python_file, [python_file]


def case_empty_directory(path_tmpdir):
    return path_tmpdir, []


def case_directory_with_one_python_file(path_tmpdir):
    one = existing_file(path_tmpdir, "one.py")
    existing_files(path_tmpdir, file_names=["two.txt", "three.txt", "four.txt"])
    return path_tmpdir, [one]


def case_directory_with_two_python_file(path_tmpdir):
    python_files = existing_files(path_tmpdir, file_names=["one.py", "two.py"])
    existing_files(path_tmpdir, file_names=["three.txt", "four.txt"])
    return path_tmpdir, python_files


def case_one_python_file_from_inner_directory(path_tmpdir):
    one = existing_file(path_tmpdir, "inner", "one.py")
    return path_tmpdir, [one]


def case_two_python_files_from_inner_directory(path_tmpdir):
    python_files = existing_files(path_tmpdir, "inner", file_names=["one.py", "two.py"])
    return path_tmpdir, python_files


def case_ignore_one_python_file(path_tmpdir):
    one = existing_file(path_tmpdir, "one.py")
    two = existing_file(path_tmpdir, "two.py")
    existing_files(path_tmpdir, file_names=["three.txt", "four.txt"])
    ignore_paths(path_tmpdir, files=[two])
    return path_tmpdir, [one]


def case_ignore_inner_directory(path_tmpdir):
    inner = path_tmpdir / "inner"
    existing_files(inner, file_names=["one.py", "two.py"])
    ignore_paths(path_tmpdir, files=[inner])
    return path_tmpdir, []


@parametrize_with_cases(argnames=["directory", "sources"], cases=THIS_MODULE)
def test_sources_finder(directory, sources):
    assert find_sources(directory) == sources
