"""Main of Eddington Static."""
import sys
from argparse import ArgumentParser
from pathlib import Path

from eddington_static import __version__
from eddington_static.command import BLACK, COMMANDS, FLAKE8, ISORT
from eddington_static.constants import DESCRIPTION

parser = ArgumentParser(description=DESCRIPTION)
parser.add_argument(
    "--version", action="version", version=__version__, help="Show version"
)
parser.add_argument("input", nargs="*", type=Path, help="Input path to analyze")
parser.add_argument(
    "--format", action="store_true", default=False, help="Format code when possible"
)
parser.add_argument(
    "--silent", action="store_true", default=False, help="Runs silently"
)
parser.add_argument(
    "--verbose", action="store_true", default=False, help="Runs verbosely"
)
parser.add_argument(
    "--fast", action="store_true", default=False, help="Include only fast actions."
)
parser.add_argument(
    "--test", action="store_true", default=False, help="Evaluate python test files",
)
parser.add_argument(
    "-c", "--commands", nargs="+", type=str, help="Specify the commands to run"
)
parser.add_argument(
    "--commands-list",
    action="store_true",
    default=False,
    help="Print list of supported commands",
)


def print_commands():
    """Print all supported commands."""
    for command in COMMANDS:
        print(command)


def print_title(title):
    """
    Print a title with a title line under it.

    :param title: The title to print
    """
    print(title.title())
    print("=" * len(title))


def main():
    """A main function of Eddington-Static."""
    args = parser.parse_args()
    if args.commands_list:
        print_commands()
        return
    input_paths = [str(path) for path in args.input]
    if len(input_paths) == 0:
        parser.print_help()
        return

    silent = args.silent
    if not silent:
        print(f"Evaluating the following files: {', '.join(input_paths)}")
    if args.fast:
        commands = [BLACK, FLAKE8, ISORT]
    else:
        commands = COMMANDS
    if args.commands:
        commands = [command for command in commands if command.name in args.commands]
    failed_commands = []
    for command in commands:
        if not silent:
            print_title(command.name)
        return_code = command.execute(
            input_paths,
            is_format=args.format,
            is_silent=silent,
            is_verbose=args.verbose,
            is_test=args.test,
        )
        if return_code != 0:
            failed_commands.append(command.name)
    print_title("Summary")
    if len(failed_commands) != 0:
        print(f"The following commands failed: {', '.join(failed_commands)}")
        sys.exit(1)
    print("Static code analysis successful")


if __name__ == "__main__":
    main()
