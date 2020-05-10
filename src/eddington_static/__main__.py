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


def run_and_throw(command, *args):
    print_title(command)
    res = subprocess.run([command, *args], env=os.environ)
    if res.returncode != 0:
        raise RuntimeError(f'"{command}" command returned with non zero return code')


def main():
    args = parser.parse_args()
    input_path = args.input
    if not isinstance(input_path, list):
        input_path = [input_path]
    input_path = [str(path) for path in input_path]

    print(f"Evaluating the following files: {', '.join(input_path)}")
    run_and_throw("black", *input_path, "--check")
    run_and_throw("flake8", *input_path, f"--config={RESOURCES_PATH / '.flake8'}")


if __name__ == "__main__":
    main()
