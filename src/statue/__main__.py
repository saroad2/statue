"""Main of Eddington Static."""
import sys
from argparse import ArgumentParser
from pathlib import Path

import toml

from statue import __version__
from statue.constants import DEFAULT_COMMANDS_FILE, DESCRIPTION
from statue.commands_reader import read_commands
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
    "-c", "--contexts", nargs="*", help="List of contexts for commands",
)
parser.add_argument(
    "-a", "--allow_list", nargs="+", type=str, help="Specify which commands to run"
)
parser.add_argument(
    "-d",
    "--deny-list",
    nargs="+",
    type=str,
    help="specify which commands to avoid running",
)
parser.add_argument(
    "-l",
    "--commands-list",
    action="store_true",
    default=False,
    help="Print list of supported commands",
)
parser.add_argument(
    "--commands-file",
    type=Path,
    default=DEFAULT_COMMANDS_FILE,
    help="Setting file to read the commands from.",
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
    commands_configuration = toml.load(args.commands_file)
    commands = read_commands(
        commands_configuration,
        contexts=args.contexts,
        allow_list=args.allow_list,
        deny_list=args.deny_list,
    )
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
