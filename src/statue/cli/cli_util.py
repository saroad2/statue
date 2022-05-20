"""Utility methods for CLI."""
from typing import List, Optional, Sequence, TypeVar

T = TypeVar("T")


def list_or_none(some_list: Optional[Sequence[T]]) -> Optional[List[T]]:
    """
    Return None if sequence is empty, else return sequence as list.

    :param some_list: Optional sequence
    :type some_list: Optional[Sequence[Any]]
    :return: None if empty, list of not
    :rtype: Optional[List[T]]
    """
    if some_list is None or len(some_list) == 0:
        return None
    return list(some_list)
