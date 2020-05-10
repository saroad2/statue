"""
This is the main module of Eddington Static
"""
import os
import subprocess
from argparse import ArgumentParser
from pathlib import Path

from eddington_static import DESCRIPTION
from eddington_static.command import Command

parser = ArgumentParser(description=DESCRIPTION)
parser.add_argument("input", nargs="+", type=Path, help="Input path to analyze")
parser.add_argument(
    "--format", action="store_true", default=False, help="Format code when possible"
)
RESOURCES_PATH = Path(__file__).parent.parent / "resources"


def print_title(title):
    """
    Prints a title with a title line under it.
    :param title: The title to print
    """
    print(title.title())
    print("=" * len(title))


def run_command(command, is_format=False):
    """
    Run an analysis command
    :param command: a :ref:`Command` class representing the command to run.
    :param is_format: Boolean. Indicates if formatting is required.
    :return: Int. Returns the return code of the command
    """
    print_title(command.name)
    args = [command.name, *command.args]
    if not is_format and command.check_arg is not None:
        args.append(command.check_arg)
    res = subprocess.run(args, env=os.environ, check=False)
    return res.returncode


def run(*commands, is_format=False):
    """
    Run all static analysis commands
    :param commands: List of commands to run
    :param is_format: Boolean. Indicates if formatting is required.
    :return: List of failed command names.
    """
    return_codes = {
        command.name: run_command(command, is_format=is_format) for command in commands
    }
    return [command for command, code in return_codes.items() if code != 0]


def main():
    """
    Main function of Eddington-Static
    """
    args = parser.parse_args()
    input_path = args.input
    if not isinstance(input_path, list):
        input_path = [input_path]
    input_path = [str(path) for path in input_path]

    print(f"Evaluating the following files: {', '.join(input_path)}")
    failed_commands = run(
        Command(name="black", args=input_path, check_arg="--check"),
        Command(
            name="flake8", args=[*input_path, f"--config={RESOURCES_PATH / '.flake8'}"]
        ),
        Command(
            name="isort",
            args=[
                *input_path,
                "--recursive",
                f"--settings-path={RESOURCES_PATH / '.isort.cfg'}",
            ],
            check_arg="--check-only",
        ),
        Command(name="pylint", args=input_path),
        is_format=args.format,
    )
    print_title("Summary")
    if len(failed_commands) == 0:
        print("Static code analysis successful")
    else:
        print(f"The following commands failed: {', '.join(failed_commands)}")


if __name__ == "__main__":
    main()
