"""Print related methods."""
from typing import Any, Callable

from statue.evaluation import Evaluation
from statue.verbosity import DEFAULT_VERBOSITY, is_silent


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


def print_evaluation(
    evaluation: Evaluation,
    verbosity: str = DEFAULT_VERBOSITY,
    print_method: Callable[..., None] = print,
):
    """
    Print evaluation in a readable way.

    :param evaluation: The evaluation to print
    :type evaluation: Evaluation
    :param verbosity: Verbosity level of the printing
    :type verbosity: str
    :param print_method: Printing method. Default is builtin print
    :type print_method: Callable[..., None]
    """
    for input_path, source_evaluation in evaluation.items():
        if not is_silent(verbosity):
            print_method("")
            print_method("")
            print_title(input_path, transform=False, print_method=print_method)
            print_method("")
        for command_evaluation in source_evaluation:
            if not is_silent(verbosity):
                print_title(
                    command_evaluation.command.name,
                    underline="-",
                    print_method=print_method,
                )
                print_method(command_evaluation.captured_output)
