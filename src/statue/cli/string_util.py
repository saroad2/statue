"""Print related methods."""
import click

from statue.cli.styled_strings import name_style, source_style
from statue.evaluation import Evaluation
from statue.verbosity import DEFAULT_VERBOSITY, is_verbose


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
    unstyled_string = click.unstyle(original_string)
    returned = (
        original_string.replace(unstyled_string, unstyled_string.title())
        if transform
        else original_string
    )
    returned += "\n" + underline * len(unstyled_string)
    return returned


def boxed_string(original_string: str, border: str = "#") -> str:
    """
    String of boxed context.

    :param original_string: The original string to wrap in box
    :type original_string: str
    :param border: Character to use as border to the text
    :type border: str
    :return: Boxed string
    :rtype: str
    """
    unstyled_string = click.unstyle(original_string)
    vertical_border = border * (len(unstyled_string) + 4)
    new_string = original_string.replace(unstyled_string, unstyled_string.title())
    middle_row = f"\n{border} {new_string} {border}\n"
    return vertical_border + middle_row + vertical_border


def evaluation_string(
    evaluation: Evaluation, verbosity: str = DEFAULT_VERBOSITY
) -> str:
    """
    Create evaluation pretty string.

    :param evaluation: The evaluation to format
    :type evaluation: Evaluation
    :param verbosity: Verbosity level of the printing
    :type verbosity: str
    :return: Evaluation as pretty string
    :rtype: str
    """
    returned = ""
    for source, source_evaluation in evaluation.items():
        source_title = title_string(source_style(source), transform=False)
        returned += f"\n\n{source_title}\n\n"
        for command_evaluation in source_evaluation:
            styled_command_name = name_style(command_evaluation.command.name)
            command_title = title_string(
                styled_command_name, underline="-", transform=False
            )
            returned += f"{command_title}\n"
            if is_verbose(verbosity):
                returned += (
                    f"{styled_command_name} ran with args: "
                    f"{command_evaluation.command.args}\n"
                    f"Finished in {command_evaluation.execution_duration:.2f} "
                    "seconds.\n"
                )
            returned += f"{command_evaluation.captured_output_string}\n"
    return returned
