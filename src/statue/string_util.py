"""Print related methods."""
from typing import Any, Callable

from statue.evaluation import Evaluation
from statue.verbosity import DEFAULT_VERBOSITY, is_silent


def title_string(
    original_string: str, underline: str = "=", transform: bool = True
) -> str:
    """
    Create a title string with underline barrier row (markdown style).

    :param original_string: The original string to turn to title
    :type original_string: str
    :param underline: Character to use as underline to the title
    :type underline: str
    :param transform: Transform first letter of each word to upper case
    :type transform: bool
    :return: Markdown title string
    :rtype: str
    """
    returned = original_string.title() if transform else original_string
    returned += "\n" + underline * len(original_string)
    return returned


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
            print_method(title_string(input_path, transform=False))
            print_method("")
        for command_evaluation in source_evaluation:
            if not is_silent(verbosity):
                print_method(
                    title_string(command_evaluation.command.name, underline="-")
                )
                print_method(command_evaluation.captured_output)
