"""Evaluation of commands map."""
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, ItemsView, Iterator, KeysView, List, Union

from statue.command import Command
from statue.print_util import print_title
from statue.verbosity import DEFAULT_VERBOSITY, is_silent


@dataclass
class CommandEvaluation:
    """Evaluation result of a command."""

    command: Command
    success: bool

    def as_json(self) -> Dict[str, Any]:
        """
        Return command evaluation as json dictionary.

        :return: Self as dictionary
        :rtype: Dict[str, Any]
        """
        command_json = {
            key: value
            for key, value in asdict(self.command).items()
            if value is not None
        }
        return dict(command=command_json, success=self.success)

    @classmethod
    def from_json(cls, command_evaluation: Dict[str, Any]) -> "CommandEvaluation":
        """
        Read command evaluation from json dictionary.

        :param command_evaluation: Json command evaluation
        :type command_evaluation: Dict[str, Any]
        :return: Parsed command evaluation
        :rtype: CommandEvaluation
        """
        return CommandEvaluation(
            command=Command(**command_evaluation["command"]),
            success=command_evaluation["success"],
        )


@dataclass
class SourceEvaluation:
    """Evaluation result of a source."""

    commands_evaluations: List[CommandEvaluation] = field(default_factory=list)

    def as_json(self) -> List[Dict[str, Any]]:
        """
        Return source evaluation as json dictionary.

        :return: Self as dictionary
        :rtype: Dict[str, Any]
        """
        return [
            command_evaluation.as_json()
            for command_evaluation in self.commands_evaluations
        ]

    @property
    def success(self) -> bool:
        """
        All commands evaluations are successful.

        :return: Success statue
        :rtype: bool
        """
        return all(
            commands_evaluation.success
            for commands_evaluation in self.commands_evaluations
        )

    @property
    def commands_number(self):
        """
        Number of commands that were evaluated.

        :return: Counted commands
        :rtype: int
        """
        return len(self.commands_evaluations)

    @property
    def successful_commands_number(self):
        """
        Number of successful commands that were evaluated.

        :return: Counted successful commands
        :rtype: int
        """
        return len(
            [
                commands_evaluation
                for commands_evaluation in self.commands_evaluations
                if commands_evaluation.success
            ]
        )

    @property
    def failed_commands_number(self):
        """
        Number of failed commands that were evaluated.

        :return: Counted failed commands
        :rtype: int
        """
        return self.commands_number - self.successful_commands_number

    @classmethod
    def from_json(cls, source_evaluation: List[Dict[str, Any]]) -> "SourceEvaluation":
        """
        Read source evaluation from json list.

        :param source_evaluation: Json commands evaluations list
        :type source_evaluation: List[Dict[str, Any]]
        :return: Parsed source evaluation
        :rtype: SourceEvaluation
        """
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

    def __iter__(self) -> Iterator[str]:
        """
        Iterate over evaluation.

        :return: self iterator
        :rtype: Iterator[str]
        """
        return iter(self.sources_evaluations)

    def __getitem__(self, item: str) -> SourceEvaluation:
        """
        Get source evaluation.

        :param item: Source name
        :type item: str
        :return: Source's evaluation
        :rtype: SourceEvaluation
        """
        return self.sources_evaluations[item]

    def __setitem__(self, key: str, value: SourceEvaluation) -> None:
        """
        Set source evaluation.

        :param key: Source name
        :type key: str
        :param value: Source's evaluation
        :type value: SourceEvaluation
        """
        self.sources_evaluations[key] = value

    def keys(self) -> KeysView[str]:
        """
        Get sources as generator.

        :return: All sources names generator
        :rtype: KeysView[str]
        """
        return self.sources_evaluations.keys()

    def items(self) -> ItemsView[str, SourceEvaluation]:
        """
        Get sources evaluations.

        :return: All sources names-instance tuples generator
        :rtype: ItemsView[str, SourceEvaluation]
        """
        return self.sources_evaluations.items()

    def as_json(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Return evaluation as json dictionary.

        :return: Self as dictionary
        :rtype: Dict[str, List[Dict[str, Any]]]
        """
        return {key: value.as_json() for key, value in self.items()}

    def save_as_json(self, output: Union[Path, str]) -> None:
        """
        Save evaluation as json.

        :param output: Path to save self in
        :type output: Path or str
        """
        with open(output, mode="w", encoding="utf-8") as output_file:
            json.dump(self.as_json(), output_file, indent=2)

    @property
    def success(self) -> bool:
        """
        All sources evaluations are successful.

        :return: Success statue
        :rtype: bool
        """
        return all(
            sources_evaluation.success
            for sources_evaluation in self.sources_evaluations.values()
        )

    @property
    def commands_number(self):
        """
        Number of commands that were evaluated.

        :return: Counted commands
        :rtype: int
        """
        return sum(
            [
                source_evaluation.commands_number
                for source_evaluation in self.sources_evaluations.values()
            ]
        )

    @property
    def successful_commands_number(self):
        """
        Number of successful commands that were evaluated.

        :return: Counted successful commands
        :rtype: int
        """
        return sum(
            [
                source_evaluation.successful_commands_number
                for source_evaluation in self.sources_evaluations.values()
            ]
        )

    @property
    def failed_commands_number(self):
        """
        Number of failed commands that were evaluated.

        :return: Counted failed commands
        :rtype: int
        """
        return self.commands_number - self.successful_commands_number

    @classmethod
    def load_from_file(cls, input_path: Path) -> "Evaluation":
        """
        Load evaluation from json file.

        :param input_path: Path to load evaluation from.
        :type input_path: Path
        :return: Evaluation instance
        :rtype: Evaluation
        """
        with open(input_path, mode="r", encoding="utf-8") as input_file:
            return Evaluation.from_json(json.load(input_file))

    @property
    def commands_map(self) -> Dict[str, List[Command]]:
        """
        Get a map from input paths to commands.

        :return: Map of commands
        :rtype: Dict[str, List[Command]]
        """
        return {
            input_path: [
                command_evaluation.command
                for command_evaluation in source_valuation.commands_evaluations
            ]
            for input_path, source_valuation in self.items()
        }

    @property
    def failure_map(self) -> Dict[str, List[Command]]:
        """
        Get a map from input paths to failed commands.

        :return: Map of failed commands
        :rtype: Dict[str, List[Command]]
        """
        failure_dict = {
            input_path: [
                command_evaluation.command
                for command_evaluation in source_valuation.commands_evaluations
                if not command_evaluation.success
            ]
            for input_path, source_valuation in self.items()
        }
        return {
            input_path: commands
            for input_path, commands in failure_dict.items()
            if len(commands) != 0
        }

    @classmethod
    def from_json(cls, evaluation: Dict[str, List[Dict[str, Any]]]) -> "Evaluation":
        """
        Read evaluation from json dictionary.

        :param evaluation: Json evaluation
        :type evaluation: List[Dict[str, Any]]]
        :return: Parsed evaluation
        :rtype: Evaluation
        """
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
    :type commands_map: Dict[str, List[Command]],
    :param verbosity: verbosity level
    :type verbosity: str
    :param print_method: print method, can be either ``print`` or ``click.echo``
    :type print_method: Callable
    :return: Evaluation
    """
    evaluation = Evaluation()
    for input_path, commands in commands_map.items():
        source_evaluation = SourceEvaluation()
        if not is_silent(verbosity):
            print_method("")
            print_method("")
            print_title(input_path, transform=False, print_method=print_method)
            print_method("")
        for command in commands:
            if not is_silent(verbosity):
                print_title(command.name, underline="-", print_method=print_method)
            success = command.execute(input_path, verbosity) == 0
            source_evaluation.commands_evaluations.append(
                CommandEvaluation(command=command, success=success)
            )
        evaluation[input_path] = source_evaluation
    return evaluation
