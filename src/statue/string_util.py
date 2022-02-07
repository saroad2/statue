"""Print related methods."""
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
    returned = original_string.title() if transform else original_string
    returned += "\n" + underline * len(original_string)
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
    vertical_border = border * (len(original_string) + 4)
    middle_row = f"\n{border} {original_string.title()} {border}\n"
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
    for input_path, source_evaluation in evaluation.items():
        returned += f"\n\n{title_string(input_path, transform=False)}\n\n"
        for command_evaluation in source_evaluation:
            command_title = title_string(
                command_evaluation.command.name, underline="-", transform=False
            )
            returned += f"{command_title}\n"
            if is_verbose(verbosity):
                returned += (
                    f"{command_evaluation.command.name} "
                    "ran with args: "
                    f"{command_evaluation.command.args}\n"
                    f"Finished in {command_evaluation.execution_duration:.2f} "
                    "seconds.\n"
                )
            returned += f"{command_evaluation.captured_output_string}\n"
    return returned
