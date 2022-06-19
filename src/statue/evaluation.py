"""Evaluation of commands map."""
import datetime
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, ItemsView, Iterator, KeysView, List, ValuesView

from statue.command import CommandEvaluation
from statue.commands_map import CommandsMap
from statue.constants import DATETIME_FORMAT, ENCODING


@dataclass
class SourceEvaluation:
    """Evaluation result of a source."""

    commands_evaluations: List[CommandEvaluation] = field(default_factory=list)
    source_execution_duration: float = field(default=0)

    def __len__(self) -> int:
        """
        Number of command evaluations.

        :return: command evaluations count
        :rtype: int
        """
        return len(self.commands_evaluations)

    def append(self, command_evaluation: CommandEvaluation) -> None:
        """
        Append new command evaluation.

        :param command_evaluation: Evaluation to be appended
        :type command_evaluation: CommandEvaluation
        """
        self.commands_evaluations.append(command_evaluation)

    def as_dict(self) -> Dict[str, Any]:
        """
        Return source evaluation as json dictionary.

        :return: Self as dictionary
        :rtype: Dict[str, Any]
        """
        return dict(
            commands_evaluations=[
                command_evaluation.as_dict()
                for command_evaluation in self.commands_evaluations
            ],
            source_execution_duration=self.source_execution_duration,
        )

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
    def from_dict(cls, source_evaluation: Dict[str, Any]) -> "SourceEvaluation":
        """
        Read source evaluation from json list.

        :param source_evaluation: Json commands evaluations list
        :type source_evaluation: List[Dict[str, Any]]
        :return: Parsed source evaluation
        :rtype: SourceEvaluation
        """
        return SourceEvaluation(
            commands_evaluations=[
                CommandEvaluation.from_dict(command_evaluation)
                for command_evaluation in source_evaluation["commands_evaluations"]
            ],
            source_execution_duration=source_evaluation["source_execution_duration"],
        )

    def __iter__(self) -> Iterator[CommandEvaluation]:
        """
        Iterate over commands evaluations.

        :return: commands evaluation iterator
        :rtype: Iterator[CommandEvaluation]
        """
        return iter(self.commands_evaluations)


@dataclass
class Evaluation:
    """Full evaluation class."""

    timestamp: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now().replace(microsecond=0)
    )
    sources_evaluations: Dict[Path, SourceEvaluation] = field(default_factory=dict)
    total_execution_duration: float = field(default=0)

    def __iter__(self) -> Iterator[Path]:
        """
        Iterate over evaluation.

        :return: self iterator
        :rtype: Iterator[Path]
        """
        return iter(self.sources_evaluations)

    def __getitem__(self, item: Path) -> SourceEvaluation:
        """
        Get source evaluation.

        :param item: Source name
        :type item: Path
        :return: Source's evaluation
        :rtype: SourceEvaluation
        """
        return self.sources_evaluations[item]

    def __setitem__(self, key: Path, value: SourceEvaluation) -> None:
        """
        Set source evaluation.

        :param key: Source name
        :type key: Path
        :param value: Source's evaluation
        :type value: SourceEvaluation
        """
        self.sources_evaluations[key] = value

    def keys(self) -> KeysView[Path]:
        """
        Get sources as generator.

        :return: All sources names generator
        :rtype: KeysView[str]
        """
        return self.sources_evaluations.keys()

    def values(self) -> ValuesView[SourceEvaluation]:
        """
        Get all source evaluations.

        :return: source evaluations list
        :rtype: ValuesView[SourceEvaluation]
        """
        return self.sources_evaluations.values()

    def items(self) -> ItemsView[Path, SourceEvaluation]:
        """
        Get sources evaluations.

        :return: All sources names-instance tuples generator
        :rtype: ItemsView[str, SourceEvaluation]
        """
        return self.sources_evaluations.items()

    def as_dict(self) -> Dict[str, Any]:
        """
        Return evaluation as json dictionary.

        :return: Self as dictionary
        :rtype: Dict[str, List[Dict[str, Any]]]
        """
        sources_evaluations = {str(key): value.as_dict() for key, value in self.items()}
        return dict(
            timestamp=self.timestamp.strftime(DATETIME_FORMAT),
            sources_evaluations=sources_evaluations,
            total_execution_duration=self.total_execution_duration,
        )

    def save_as_json(self, output: Path) -> None:
        """
        Save evaluation as json.

        :param output: Path to save self in
        :type output: Path
        """
        with open(output, mode="w", encoding=ENCODING) as output_file:
            json.dump(self.as_dict(), output_file, indent=2)

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
            source_evaluation.commands_number
            for source_evaluation in self.sources_evaluations.values()
        )

    @property
    def successful_commands_number(self):
        """
        Number of successful commands that were evaluated.

        :return: Counted successful commands
        :rtype: int
        """
        return sum(
            source_evaluation.successful_commands_number
            for source_evaluation in self.sources_evaluations.values()
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
        with open(input_path, mode="r", encoding=ENCODING) as input_file:
            return Evaluation.from_dict(json.load(input_file))

    @property
    def commands_map(self) -> CommandsMap:
        """
        Get a map from input paths to commands.

        :return: Map of commands
        :rtype: CommandsMap
        """
        return CommandsMap(
            {
                input_path: [
                    command_evaluation.command
                    for command_evaluation in source_valuation.commands_evaluations
                ]
                for input_path, source_valuation in self.items()
            }
        )

    @property
    def failure_evaluation(self) -> "Evaluation":
        """
        Returns a new evaluation map with only failed commands.

        :return: Map of failed commands
        :rtype: Evaluation
        """
        failure_dict = {
            source: SourceEvaluation(
                [
                    command_evaluation
                    for command_evaluation in source_evaluation.commands_evaluations
                    if not command_evaluation.success
                ]
            )
            for source, source_evaluation in self.items()
        }
        failure_dict = {
            source: source_evaluation
            for source, source_evaluation in failure_dict.items()
            if len(source_evaluation) != 0
        }
        return Evaluation(
            timestamp=self.timestamp,
            sources_evaluations=failure_dict,
            total_execution_duration=self.total_execution_duration,
        )

    @classmethod
    def from_dict(cls, evaluation: Dict[str, Any]) -> "Evaluation":
        """
        Read evaluation from json dictionary.

        :param evaluation: Json evaluation
        :type evaluation: List[Dict[str, Any]]]
        :return: Parsed evaluation
        :rtype: Evaluation
        """
        return Evaluation(
            timestamp=datetime.datetime.strptime(
                evaluation["timestamp"], DATETIME_FORMAT
            ),
            sources_evaluations={
                Path(input_path): SourceEvaluation.from_dict(source_evaluation)
                for input_path, source_evaluation in evaluation[
                    "sources_evaluations"
                ].items()
            },
            total_execution_duration=evaluation["total_execution_duration"],
        )
