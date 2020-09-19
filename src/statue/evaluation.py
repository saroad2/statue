"""Evaluation of commands map."""
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Dict, List

from statue.command import Command
from statue.print_util import print_title
from statue.verbosity import DEFAULT_VERBOSITY, is_silent


@dataclass
class CommandEvaluation:
    """Evaluation result of a command."""

    command: Command
    success: bool

    def as_json(self):
        return dict(command=asdict(self.command), success=self.success)

    @classmethod
    def from_json(cls, command_evaluation):
        return CommandEvaluation(
            command=Command(**command_evaluation["command"]),
            success=command_evaluation["success"],
        )


@dataclass
class SourceEvaluation:
    """Evaluation result of a source."""

    commands_evaluations: List[CommandEvaluation] = field(default_factory=list)

    def as_json(self):
        return [
            command_evaluation.as_json()
            for command_evaluation in self.commands_evaluations
        ]

    @classmethod
    def from_json(cls, source_evaluation):
        return SourceEvaluation(
            commands_evaluations=[
                CommandEvaluation.from_json(command_evaluation)
                for command_evaluation in source_evaluation
            ]
        )


@dataclass
class Evaluation:
    """Full evaluation class."""

    sources_evaluations: Dict[str, SourceEvaluation] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.sources_evaluations)

    def __getitem__(self, item):
        return self.sources_evaluations[item]

    def __setitem__(self, key, value):
        self.sources_evaluations[key] = value

    def items(self):
        return self.sources_evaluations.items()

    def as_json(self):
        return {key: value.as_json() for key, value in self.items()}

    def save_as_json(self, output: Path):
        with open(output, mode="w") as output_file:
            json.dump(self.as_json(), output_file, indent=2)

    @classmethod
    def load_from_json(cls, input_path: Path):
        with open(input_path, mode="r") as input_file:
            return Evaluation.from_json(json.load(input_file))

    @classmethod
    def from_json(cls, evaluation):
        return Evaluation(
            sources_evaluations={
                input_path: SourceEvaluation.from_json(source_evaluation)
                for input_path, source_evaluation in evaluation.items()
            }
        )


def evaluate_commands_map(
    commands_map: Dict[str, List[Command]],
    verbosity: str = DEFAULT_VERBOSITY,
    print_method: Callable[..., None] = print,
) -> Evaluation:
    """
    Run commands map and return evaluation report.

    :param commands_map: map from input file to list of commands to run on it,
    :param verbosity: verbosity level
    :param print_method: print method, can be either ``print`` or ``click.echo``
    :return: :class:`Evaluation`
    """
    evaluation = Evaluation()
    for input_path, commands in commands_map.items():
        source_evaluation = SourceEvaluation()
        if not is_silent(verbosity):
            print_method()
            print_method(f"Evaluating {input_path}")
        for command in commands:
            if not is_silent(verbosity):
                print_title(command.name, underline="-")
            success = command.execute(input_path, verbosity) == 0
            source_evaluation.commands_evaluations.append(
                CommandEvaluation(command=command, success=success)
            )
        evaluation[input_path] = source_evaluation
    return evaluation


def get_failure_map(evaluation: Evaluation) -> Dict[str, List[Command]]:
    """
    Get a map from input paths to failed commands.

    :param evaluation: evaluation result
    :return: ``Dict[str, List[str]]``
    """
    failure_dict = dict()
    for input_path, source_valuation in evaluation.items():
        failed_commands = [
            command_evaluation.command
            for command_evaluation in source_valuation.commands_evaluations
            if not command_evaluation.success
        ]
        if len(failed_commands) != 0:
            failure_dict[input_path] = failed_commands
    return failure_dict
