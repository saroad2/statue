from pathlib import Path

from statue.io_util import is_equal_or_child_of


def test_child_is_child_of_itself(tmp_path):
    source = tmp_path / "a"
    assert is_equal_or_child_of(source, source)


def test_child_is_child_of_parent(tmp_path):
    source1 = tmp_path / "a" / "b"
    source2 = tmp_path / "a"
    assert is_equal_or_child_of(source1, source2)


def test_child_is_child_of_grandparent(tmp_path):
    source1 = tmp_path / "a" / "b" / "c"
    source2 = tmp_path / "a"
    assert is_equal_or_child_of(source1, source2)


def test_child_is_child_of_cwd(tmp_path):
    source1 = Path("a") / "b"
    source2 = Path.cwd() / "a"
    assert is_equal_or_child_of(source1, source2)


def test_child_is_not_child_of_sibling(tmp_path):
    source1 = tmp_path / "b"
    source2 = tmp_path / "a"
    assert not is_equal_or_child_of(source1, source2)
