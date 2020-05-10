import os
from argparse import ArgumentParser
from pathlib import Path
import subprocess

from eddington_static import description
from eddington_static.command import Command

parser = ArgumentParser(description=description)
parser.add_argument("input", nargs="+", type=Path, help="Input path to analyze")
parser.add_argument(
    "--format", action="store_true", default=False, help="Format code when possible"
)
RESOURCES_PATH = Path(__file__).parent.parent / "resources"


def print_title(title):
    print(title.title())
    print("=" * len(title))


def run_command(command, is_format=False):
    print_title(command.name)
    args = list(command.args)
    if not is_format and command.check_arg is not None:
        args.append(command.check_arg)
    res = subprocess.run([command.name, *args], env=os.environ)
    return res.returncode


def run(*commands, is_format=False):
    return_codes = {
        command.name: run_command(command, is_format=is_format) for command in commands
    }
    return [command for command, code in return_codes.items() if code != 0]


def main():
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
        is_format=args.format,
    )
    print_title("Summary")
    if len(failed_commands) == 0:
        print("Static code analysis successful")
    else:
        print(f"The following commands failed: {', '.join(failed_commands)}")


if __name__ == "__main__":
    main()
