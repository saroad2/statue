"""Print related methods."""
from typing import Any, Callable


def print_title(
    title: str,
    underline: str = "=",
    transform: bool = True,
    print_method: Callable[[Any], None] = print,
) -> None:
    """
    Print a title with a title line under it.

    :param title: The title to print
    :param underline: Character to use as underline to the title
    :param transform: Transform first letter of each word to upper case
    :param print_method: print method, can be either ``print`` or ``click.echo``
    """
    if transform:
        title = title.title()
    print_method(title)
    print_method(underline * len(title))


def print_boxed(
    title: str,
    border: str = "#",
    print_method: Callable[[Any], None] = print,
) -> None:
    """
    Print boxed context.

    :param title: The title to print
    :param border: Character to use as border to the text
    :param print_method: print method, can be either ``print`` or ``click.echo``
    """
    print_method(border * (len(title) + 4))
    print_method(f"{border} {title.title()} {border}")
    print_method(border * (len(title) + 4))
