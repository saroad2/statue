"""Main of Eddington Static."""
import sys
from argparse import ArgumentParser
from pathlib import Path

from eddington_static.command import create_commands
from eddington_static.constants import DESCRIPTION

parser = ArgumentParser(description=DESCRIPTION)
parser.add_argument("input", nargs="+", type=Path, help="Input path to analyze")
parser.add_argument(
    "--format", action="store_true", default=False, help="Format code when possible"
)
parser.add_argument(
    "--silent", action="store_true", default=False, help="Runs silently"
)
parser.add_argument(
    "-c", "--commands", nargs="+", type=str, help="Specify the commands to run"
)


def print_title(title):
    """
    Print a title with a title line under it.

    :param title: The title to print
    """
    print(title.title())
    print("=" * len(title))


def run(commands, is_format=False, is_silent=False):
    """
    Run all static analysis commands.

    :param commands: List of commands to run
    :param is_format: Boolean. Indicates if formatting is required.
    :param is_silent: Boolean. Indicates to run the command without capturing
     output.
    :return: List of failed command names.
    """
    failed_commands = []
    for command in commands:
        if not is_silent:
            print_title(command.name)
        return_code = command.execute(is_format=is_format, is_silent=is_silent)
        if return_code != 0:
            failed_commands.append(command.name)
    return failed_commands


def main():
    """A main function of Eddington-Static."""
    args = parser.parse_args()
    input_path = [str(path) for path in args.input]

    silent = args.silent
    if not silent:
        print(f"Evaluating the following files: {', '.join(input_path)}")
    commands = create_commands(input_path)
    if args.commands:
        commands = [command for command in commands if command.name in args.commands]
    failed_commands = run(commands, is_format=args.format, is_silent=silent,)
    print_title("Summary")
    if len(failed_commands) != 0:
        print(f"The following commands failed: {', '.join(failed_commands)}")
        sys.exit(1)
    print("Static code analysis successful")


if __name__ == "__main__":
    main()
