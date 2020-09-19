"""Print related methods."""
from typing import Any, Callable


def print_title(
    title: str,
    underline: str = "=",
    print_method: Callable[[Any], None] = print,
) -> None:
    """
    Print a title with a title line under it.

    :param underline: Character to use as underline to the title
    :param title: The title to print
    :param print_method: print method, can be either ``print`` or ``click.echo``
    """
    print_method(title.title())
    print_method(underline * len(title))
