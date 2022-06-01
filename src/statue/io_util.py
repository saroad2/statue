"""Utility methods related to Input/Output."""
from pathlib import Path


def is_equal_or_child_of(source1: Path, source2: Path) -> bool:
    """
    Checking if a source equal or a child of another source.

    :param source1: Child source to check
    :type source1: Path
    :param source2: Parent source to check
    :type source2: Path
    :return: Is sources1 relative to source2
    :rtype: bool
    """
    source1, source2 = source1.absolute(), source2.absolute()
    if source2 == source1:
        return True
    return source2 in source1.parents
