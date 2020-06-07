"""Main of Eddington Static."""
import sys
from argparse import ArgumentParser
from pathlib import Path

from statue import __version__
from statue.constants import DEFAULT_COMMANDS_FILE, DESCRIPTION
from statue.reader import read_commands
from statue.validations import validate

parser = ArgumentParser(description=DESCRIPTION)
parser.add_argument(
    "--version", action="version", version=__version__, help="Show version"
)
parser.add_argument("input", nargs="*", type=Path, help="Input path to analyze")
parser.add_argument(
    "--silent", action="store_true", default=False, help="Runs silently"
)
parser.add_argument(
    "--verbose", action="store_true", default=False, help="Runs verbosely"
)
parser.add_argument(
    "-f", "--filters", nargs="*", help="List of filters for commands",
)
parser.add_argument(
    "-c", "--commands", nargs="+", type=str, help="Specify the commands to run"
)
parser.add_argument(
    "-r", "--remove", nargs="+", type=str, help="Remove commands from running"
)
parser.add_argument(
    "-s",
    "--settings",
    type=Path,
    default=DEFAULT_COMMANDS_FILE,
    help="Setting file to read the commands from.",
)
parser.add_argument(
    "--commands-list",
    action="store_true",
    default=False,
    help="Print list of supported commands",
)


def print_commands(commands) -> None:
    """Print all supported commands."""
    for command in commands:
        print(command.name, "-", command.help)


def print_title(title: str) -> None:
    """
    Print a title with a title line under it.

    :param title: The title to print
    """
    print(title.title())
    print("=" * len(title))


def main() -> None:
    """A main function of Eddington-Static."""
    args = parser.parse_args()
    validate(args)
    commands = read_commands(args.settings, filters=args.filters)
    if args.commands_list:
        print_commands(commands)
        return
    input_paths = [str(path) for path in args.input]
    if len(input_paths) == 0:
        parser.print_help()
        return

    silent = args.silent
    if not silent:
        print(f"Evaluating the following files: {', '.join(input_paths)}")
    if args.commands:
        commands = [command for command in commands if command.name in args.commands]
    if args.remove:
        commands = [command for command in commands if command.name not in args.remove]
    failed_commands = []
    for command in commands:
        if not silent:
            print_title(command.name)
        return_code = command.execute(
            input_paths, is_silent=silent, is_verbose=args.verbose
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
