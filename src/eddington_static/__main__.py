import os
from argparse import ArgumentParser
from pathlib import Path
import subprocess

from eddington_static import description

parser = ArgumentParser(description=description)
parser.add_argument(
    "-i", "--input", required=True, type=Path, help="Input path to analyze"
)


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
    input_path = str(args.input.absolute())

    run_and_throw("black", input_path, "--check")
    run_and_throw("flake8", input_path, "--max-line-length=88")


if __name__ == "__main__":
    main()
