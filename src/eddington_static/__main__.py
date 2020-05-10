import os
from argparse import ArgumentParser
from pathlib import Path
import subprocess

from eddington_static import description

parser = ArgumentParser(description=description)
parser.add_argument(
    "-i", "--input", nargs="+", required=True, type=Path, help="Input path to analyze"
)
RESOURCES_PATH = Path(__file__).parent.parent / "resources"


def print_title(title):
    print(title.title())
    print("=" * len(title))


def run_command(command, *args):
    print_title(command)
    res = subprocess.run([command, *args], env=os.environ)
    return res.returncode


def run(*commands):
    return_codes = {command[0]: run_command(*command) for command in commands}
    return [command for command, code in return_codes.items() if code != 0]


def main():
    args = parser.parse_args()
    input_path = args.input
    if not isinstance(input_path, list):
        input_path = [input_path]
    input_path = [str(path) for path in input_path]

    print(f"Evaluating the following files: {', '.join(input_path)}")
    failed_commands = run(
        ["black", *input_path, "--check"],
        ["flake8", *input_path, f"--config={RESOURCES_PATH / '.flake8'}"],
        [
            "isort",
            *input_path,
            "--recursive",
            f"--settings-path={RESOURCES_PATH / '.isort.cfg'}",
            "--check-only",
        ],
    )
    print_title("Summary")
    if len(failed_commands) == 0:
        print("Static code analysis successful")
    else:
        print(f"The following commands failed: {', '.join(failed_commands)}")


if __name__ == "__main__":
    main()
