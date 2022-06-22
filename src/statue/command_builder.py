"""Build commands from configuration."""
# pylint: disable=too-many-public-methods,too-many-arguments
# pylint: disable=too-many-instance-attributes
import importlib
import itertools
import os
import subprocess  # nosec
import sys
from collections import OrderedDict
from typing import Any, Dict, Iterable, List, Optional
from typing import OrderedDict as OrderedDictType
from typing import Set

import pkg_resources

from statue.command import Command
from statue.config.contexts_repository import ContextsRepository
from statue.constants import (
    ALLOWED_CONTEXTS,
    ARGS,
    DENIED_CONTEXTS,
    HELP,
    REQUIRED_CONTEXTS,
    VERSION,
)
from statue.context import Context
from statue.context_specification import ContextSpecification
from statue.exceptions import (
    InconsistentConfiguration,
    InvalidCommand,
    InvalidConfiguration,
    MissingHelpString,
    StatueConfigurationError,
    UnknownContext,
)
from statue.verbosity import DEFAULT_VERBOSITY, is_silent


class CommandBuilder:
    """Command builder as specified in configuration."""

    def __init__(
        self,
        name: str,
        help: str,  # pylint: disable=redefined-builtin
        default_args: Optional[List[str]] = None,
        version: Optional[str] = None,
        required_contexts: Optional[Iterable[Context]] = None,
        allowed_contexts: Optional[Iterable[Context]] = None,
        denied_contexts: Optional[Iterable[Context]] = None,
        contexts_specifications: Optional[Dict[Context, ContextSpecification]] = None,
    ):
        """
        Constructor.

        :param name: Name of the command to be built by the builder
        :type name str
        :param help: Help string to describe the command
        :type help: str
        :param default_args: Optional default arguments to be added to the command
        :type default_args: Optional[List[str]]
        :param version: Optional version specification for the command builder
        :type version: Optional[str]
        :param required_contexts: Optional list of contexts required by
            the command builder
        :type required_contexts: Optional[List[Context]]
        :param allowed_contexts: Optional list of contexts allowed for
            the command builder
        :type allowed_contexts: Optional[List[Context]]
        :param denied_contexts: Optional list of contexts denied for
            the command builder
        :type denied_contexts: Optional[List[Context]]
        :param contexts_specifications: Optional dictionary of contexts specification
            for the command builder
        :type contexts_specifications: Optional[Dict[Context, ContextSpecification]]
        """
        self.name = name
        self.help = help
        self.default_args = default_args if default_args is not None else []
        self.version = version

        self._initialize_contexts()
        self.required_contexts = (
            set(required_contexts) if required_contexts is not None else set()
        )
        self.allowed_contexts = (
            set(allowed_contexts) if allowed_contexts is not None else set()
        )
        self.denied_contexts = (
            set(denied_contexts) if denied_contexts is not None else set()
        )
        self.contexts_specifications = (
            contexts_specifications if contexts_specifications is not None else {}
        )

    @property
    def required_contexts(self) -> Set[Context]:
        """Get contexts required by command builder."""
        return self._required_contexts

    @required_contexts.setter
    def required_contexts(self, required_contexts):
        """
        Set contexts required by command builder.

        :param required_contexts: Required contexts to be set.
        :type required_contexts: Set[Context]
        """
        required_contexts = set(required_contexts)
        if len(required_contexts) != 0:
            self._validate_consistency(
                allowed=self.allowed_contexts,
                denied=self.denied_contexts,
                required=required_contexts,
                specified=self.specified_contexts,
            )
        self._required_contexts = required_contexts

    @property
    def allowed_contexts(self) -> Set[Context]:
        """Get contexts allowed for command builder."""
        return self._allowed_contexts

    @allowed_contexts.setter
    def allowed_contexts(self, allowed_contexts):
        """
        Set contexts allowed for command builder.

        :param allowed_contexts: Allowed contexts to be set
        :type allowed_contexts: Set[Context]
        """
        allowed_contexts = set(allowed_contexts)
        if len(allowed_contexts) != 0:
            self._validate_consistency(
                allowed=allowed_contexts,
                denied=self.denied_contexts,
                required=self.required_contexts,
                specified=self.specified_contexts,
            )
        self._allowed_contexts = allowed_contexts

    @property
    def denied_contexts(self) -> Set[Context]:
        """Get contexts allowed for command builder."""
        return self._denied_contexts

    @denied_contexts.setter
    def denied_contexts(self, denied_contexts):
        denied_contexts = set(denied_contexts)
        if len(denied_contexts) != 0:
            self._validate_consistency(
                allowed=self.allowed_contexts,
                denied=denied_contexts,
                required=self.required_contexts,
                specified=self.specified_contexts,
            )
        self._denied_contexts = denied_contexts

    @property
    def contexts_specifications(self) -> Dict[Context, ContextSpecification]:
        """Get contexts specification dictionary for command builder."""
        return self._contexts_specifications

    @contexts_specifications.setter
    def contexts_specifications(self, contexts_specifications):
        """
        Set contexts specification dictionary for command builder.

        :param contexts_specifications: Contexts specification dictionary to be set
        :type contexts_specifications: Dict[Context, ContextSpecification]
        """
        if len(contexts_specifications) != 0:
            self._validate_consistency(
                allowed=self.allowed_contexts,
                denied=self.denied_contexts,
                required=self.required_contexts,
                specified=set(contexts_specifications.keys()),
            )
        self._contexts_specifications = contexts_specifications

    def __repr__(self) -> str:
        """
        Represent context as string.

        :return: String representation of command builder
        :rtype: str
        """
        required_contexts = [context.name for context in self.required_contexts]
        required_contexts.sort()
        allowed_contexts = [context.name for context in self.allowed_contexts]
        allowed_contexts.sort()
        denied_contexts = [context.name for context in self.denied_contexts]
        denied_contexts.sort()
        contexts_specification = {
            context.name: specification
            for context, specification in self.contexts_specifications.items()
        }
        return (
            "CommandBuilder("
            f"name={self.name}, "
            f"help={self.help}, "
            f"default_args={self.default_args}, "
            f"version={self.version}, "
            f"required_contexts={required_contexts}, "
            f"allowed_contexts={allowed_contexts}, "
            f"denied_contexts={denied_contexts}, "
            f"contexts_specifications={contexts_specification}"
            ")"
        )

    def __eq__(self, other: object) -> bool:
        """
        Check equality of this command builder with other object.

        :param other: Object to compare to
        :type other: object
        :return: is equal to self
        :rtype: bool
        """
        return (
            isinstance(other, CommandBuilder)
            and self.name == other.name
            and self.help == other.help
            and self.default_args == other.default_args
            and self.version == other.version
            and self.allowed_contexts == other.allowed_contexts
            and self.denied_contexts == other.denied_contexts
            and self.required_contexts == other.required_contexts
            and self.contexts_specifications == other.contexts_specifications
        )

    @property
    def install_name(self) -> str:
        """
        Name to state while installing with pip.

        When installing a specific version with pip, one should add "==" with the
        specific version afterwards.

        If no version is specified, same as name.

        :return: name and version
        :rtype: str
        """
        if self.version is None:
            return self.name
        return f"{self.name}=={self.version}"

    @property
    def installed_version(self) -> Optional[str]:
        """
        Version of the installed package.

        Might not be the same as the version attribute.

        :return: version of installed package
        :rtype: str or None
        """
        package = self._get_package()
        if package is None:
            return None
        return package.version

    @property
    def specified_contexts(self) -> Set[Context]:
        """Contexts names list with arguments specifications."""
        return set(self.contexts_specifications.keys())

    @property
    def available_contexts(self) -> Set[Context]:
        """Contexts which are available to use according to this command."""
        return {
            *self.required_contexts,
            *self.allowed_contexts,
            *self.specified_contexts,
        }

    def reset_all_contexts(self):
        """Reset all available contexts."""
        self.required_contexts = []
        self.allowed_contexts = []
        self.denied_contexts = []
        self.contexts_specifications = {}

    def installed(self) -> bool:
        """
        Is this command installed.

        :return: Either the command is installed or not
        :rtype: bool
        """
        return self.installed_version is not None

    def set_version_as_installed(self):
        """
        Set version to be the installed version.

        PAY ATTENTION: if command is not installed, version will be set to None
        """
        self.version = self.installed_version

    def installed_correctly(self) -> bool:
        """
        Checks that command is installed and its version matches.

        :return: whether the command is installed correctly
        :rtype: bool
        """
        return self.installed() and self.installed_version_match()

    def installed_version_match(self) -> bool:
        """
        Is the installed version match the specified version.

        :return: is the installed version matches the desired version
        :rtype: bool
        """
        if self.version is None:
            return True
        return self.installed_version == self.version

    def install(self, verbosity: str = DEFAULT_VERBOSITY) -> None:
        """
        Install command using pip.

        :param verbosity: Verbosity level.
        :type verbosity: str
        """
        if self.installed():
            return
        if not is_silent(verbosity):
            print(f"Installing {self.install_name}")
        subprocess.run(  # nosec
            [sys.executable, "-m", "pip", "install", self.install_name],
            env=os.environ,
            check=False,
            capture_output=is_silent(verbosity),
        )

    def update(self, verbosity: str = DEFAULT_VERBOSITY) -> None:
        """
        Update command using pip.

        :param verbosity: Verbosity level.
        :type verbosity: str
        """
        if not is_silent(verbosity):
            print(f"Updating {self.name}")
        subprocess.run(  # nosec
            [sys.executable, "-m", "pip", "install", "-U", self.name],
            env=os.environ,
            check=False,
            capture_output=is_silent(verbosity),
        )

    def uninstall(self, verbosity: str = DEFAULT_VERBOSITY) -> None:
        """
        Uninstall command using pip.

        :param verbosity: Verbosity level.
        :type verbosity: str
        """
        if not self.installed():
            return
        if not is_silent(verbosity):
            print(f"Uninstalling {self.name} (version {self.installed_version})")
        subprocess.run(  # nosec
            [sys.executable, "-m", "pip", "uninstall", "-y", self.name],
            env=os.environ,
            check=False,
            capture_output=is_silent(verbosity),
        )

    def update_to_version(self, verbosity=DEFAULT_VERBOSITY) -> None:
        """
        Update command to the specified version using pip.

        If the installed version is the same as version, do nothing.

        :param verbosity: Verbosity level.
        :type verbosity: str
        """
        if not self.installed():
            self.install(verbosity=verbosity)
            return
        if self.version is None:
            # If no version is specified, we update package to its latest version
            self.update(verbosity=verbosity)
            return
        if self.installed_version_match():
            return
        # If a version is specified, we must first uninstall it
        # before installing the specified version.
        self.uninstall(verbosity=verbosity)
        self.install(verbosity=verbosity)

    def validate_contexts_match(self, *contexts: Context):
        """
        Validate that given contexts are matching command builder.

        :param contexts: Specified contexts to check matching.
        :type contexts: Context
        :raises InvalidCommand: Raised when given contexts doesn't match
            the command's requirements
        """
        missing_required_contexts = [
            required_context.name
            for required_context in self.required_contexts
            if all(
                context != required_context
                and not context.is_child_of(required_context)
                for context in contexts
            )
        ]
        if len(missing_required_contexts) != 0:
            raise InvalidCommand(
                f"Command `{self.name}` "
                "requires the following contexts, which are missing: "
                f"{', '.join(missing_required_contexts)}"
            )
        explicitly_denied_contexts = [
            context.name
            for context in contexts
            if any(
                context == denied_context or context.is_child_of(denied_context)
                for denied_context in self.denied_contexts
            )
        ]
        if len(explicitly_denied_contexts) != 0:
            raise InvalidCommand(
                f"Command `{self.name}` "
                "denies the following contexts, which are present: "
                f"{', '.join(explicitly_denied_contexts)}"
            )
        not_allowed_contexts = [
            context.name
            for context in contexts
            if not context.allowed_by_default
            and all(
                context != available_context
                and not context.is_child_of(available_context)
                for available_context in self.available_contexts
            )
        ]
        if len(not_allowed_contexts) != 0:
            raise InvalidCommand(
                f"Command `{self.name}` "
                "is not allowed due to the following contexts: "
                f"{', '.join(not_allowed_contexts)}"
            )

    def match_contexts(self, *contexts: Context) -> bool:
        """
        Check if given contexts are matching builder.

        :param contexts: Specified contexts to check matching.
        :type contexts: Context
        :return: does those contexts match builder
        :rtype: bool
        """
        try:
            self.validate_contexts_match(*contexts)
        except InvalidCommand:
            return False
        return True

    def remove_context(self, context: Context):
        """
        Remove context reference from builder.

        :param context: Context to be removed
        :type context: Context
        """
        if context in self.required_contexts:
            self.required_contexts.remove(context)
        if context in self.allowed_contexts:
            self.allowed_contexts.remove(context)
        if context in self.denied_contexts:
            self.denied_contexts.remove(context)
        if context in self.contexts_specifications:
            self.contexts_specifications.pop(context)

    def build_command(self, *contexts: Context) -> Command:
        """
        Build command according to given contexts.

        :param contexts: Specified contexts to build command according to.
        :type contexts: Context
        :return: Built command.
        :rtype: Command
        """
        self.validate_contexts_match(*contexts)
        return Command(name=self.name, args=self.build_args(*contexts))

    def build_args(self, *contexts: Context) -> List[str]:
        """
        Build arguments for command according to contexts.

        :param contexts: Specified contexts to arguments
            command according to.
        :type contexts: Context
        :return: Arguments list
        :rtype: List[str]
        """
        args = list(self.default_args)
        for context in contexts:
            args = self.get_context_specification(context).update_args(args)
        return args

    def get_context_specification(self, context: Context) -> ContextSpecification:
        """
        Get context specification from context name.

        :param context: Specified context
        :type context: Context
        :return: Context specification to build command according to
        :rtype: ContextSpecification
        """
        return self.contexts_specifications.get(context, ContextSpecification())

    def as_dict(self) -> OrderedDictType[str, Any]:
        """
        Encode command builder as a dictionary.

        This is used in order to serialize the command builder in
        a configuration file.

        :return: Serialized representation dictionary
        :rtype: OrderedDict[str, Any]
        """
        builder_as_dict: OrderedDict[str, Any] = OrderedDict()
        builder_as_dict[HELP] = self.help
        if len(self.default_args) != 0:
            builder_as_dict[ARGS] = self.default_args
        if len(self.required_contexts) != 0:
            required_contexts = [context.name for context in self.required_contexts]
            required_contexts.sort()
            builder_as_dict[REQUIRED_CONTEXTS] = required_contexts
        if len(self.allowed_contexts) != 0:
            allowed_contexts = [context.name for context in self.allowed_contexts]
            allowed_contexts.sort()
            builder_as_dict[ALLOWED_CONTEXTS] = allowed_contexts
        if len(self.denied_contexts) != 0:
            denied_contexts = [context.name for context in self.denied_contexts]
            denied_contexts.sort()
            builder_as_dict[DENIED_CONTEXTS] = denied_contexts
        if self.version is not None:
            builder_as_dict[VERSION] = self.version
        specified_contexts = list(self.specified_contexts)
        specified_contexts.sort(key=lambda context: context.name)
        for context in specified_contexts:
            builder_as_dict[context.name] = self.contexts_specifications[
                context
            ].as_dict()
        return builder_as_dict

    @classmethod
    def from_dict(
        cls,
        command_name: str,
        builder_setups: Dict[str, Any],
        contexts_repository: ContextsRepository,
    ):
        """
        Build command builder according to a given configuration.

        :param command_name: Name of the command to be built
        :type command_name: str
        :param builder_setups: Command builder configuration
        :type builder_setups: Dict[str, Any]
        :param contexts_repository: contexts repository to get contexts from
        :type contexts_repository: ContextsRepository
        :return: Command builder as specified
        :rtype: CommandBuilder
        :raises MissingHelpString: Raised when help string is missing
        """
        if HELP not in builder_setups:
            raise MissingHelpString(location=[command_name])
        return CommandBuilder(
            name=command_name,
            help=builder_setups[HELP],
            default_args=builder_setups.get(ARGS, []),
            version=builder_setups.get(VERSION),
            required_contexts=cls.build_contexts_list(
                command_name=command_name,
                key_name=REQUIRED_CONTEXTS,
                builder_setups=builder_setups,
                contexts_repository=contexts_repository,
            ),
            allowed_contexts=cls.build_contexts_list(
                command_name=command_name,
                key_name=ALLOWED_CONTEXTS,
                builder_setups=builder_setups,
                contexts_repository=contexts_repository,
            ),
            denied_contexts=cls.build_contexts_list(
                command_name=command_name,
                key_name=DENIED_CONTEXTS,
                builder_setups=builder_setups,
                contexts_repository=contexts_repository,
            ),
            contexts_specifications=cls.build_contexts_specifications(
                command_name=command_name,
                builder_setups=builder_setups,
                contexts_repository=contexts_repository,
            ),
        )

    @classmethod
    def build_contexts_list(
        cls,
        command_name: str,
        key_name: str,
        builder_setups: Dict[str, Any],
        contexts_repository: ContextsRepository,
    ) -> List[Context]:
        """
        Read contexts list from dictionary.

        :param command_name: Name of the command to be built
        :type command_name: str
        :param key_name: Key of the desired contexts list
        :type key_name: str
        :param builder_setups: Command builder configuration
        :type builder_setups: Dict[str, Any]
        :param contexts_repository: contexts repository to get contexts from
        :type contexts_repository: ContextsRepository
        :return: Contexts list
        :rtype: List[Context]
        :raises InvalidConfiguration: Raised when one of the contexts was not
            set in the contexts repository
        """
        if key_name not in builder_setups:
            return []
        context_names = builder_setups[key_name]
        try:
            return [contexts_repository[context_name] for context_name in context_names]
        except UnknownContext as error:
            raise InvalidConfiguration(
                message="Unknown context in configuration",
                location=[command_name, key_name, error.context_name],
            ) from error

    @classmethod
    def build_contexts_specifications(
        cls,
        command_name: str,
        builder_setups: Dict[str, Any],
        contexts_repository: ContextsRepository,
    ) -> Dict[Context, ContextSpecification]:
        """
        Read command builder's contexts specifications dictionary from configuration.

        :param command_name: Name of the command to be built
        :type command_name: str
        :param builder_setups: Command builder configuration
        :type builder_setups: Dict[str, Any]
        :param contexts_repository: contexts repository to get contexts from
        :type contexts_repository: ContextsRepository
        :return: Contexts specifications dictionary
        :rtype: Dict[Context, ContextSpecification]
        :raises InvalidConfiguration: Raised when one of the contexts was not
            set in the contexts repository
        :raises StatueConfigurationError: Raised when there is an inconsistency
            in a context specification definition.
        """
        context_names = [
            context_name
            for context_name in builder_setups.keys()
            if context_name not in cls.setup_words()
        ]
        contexts_specifications = {}
        for context_name in context_names:
            try:
                contexts_specifications[
                    contexts_repository[context_name]
                ] = ContextSpecification.from_dict(
                    context_specification_setups=builder_setups[context_name]
                )
            except UnknownContext as error:
                raise InvalidConfiguration(
                    message="Unknown context in configuration",
                    location=[command_name, error.context_name],
                ) from error
            except StatueConfigurationError as error:
                error.append_location_item(context_name)
                error.append_location_item(command_name)
                raise error
        return contexts_specifications

    @classmethod
    def setup_words(cls) -> List[str]:
        """
        Predefined setup words.

        :return: List of predefined setup words
        :rtype: List[str]
        """
        return [
            HELP,
            ARGS,
            VERSION,
            ALLOWED_CONTEXTS,
            DENIED_CONTEXTS,
            REQUIRED_CONTEXTS,
        ]

    def _validate_consistency(self, **kwargs: Set[Context]):
        assert set(kwargs.keys()) == {  # nosec
            "allowed",
            "denied",
            "required",
            "specified",
        }
        for key1, key2 in itertools.combinations(kwargs.keys(), 2):
            value1, value2 = kwargs[key1], kwargs[key2]
            values_intersection = value1.intersection(value2)
            if len(values_intersection) != 0:
                self._raise_inconsistency_error(
                    type1=key1,
                    type2=key2,
                    contexts=values_intersection,
                )

    def _raise_inconsistency_error(
        self, type1: str, type2: str, contexts: Set[Context]
    ):
        context_names = [context.name for context in contexts]
        context_names.sort()
        message = f"{type1} and {type2} contexts clash"
        location = [self.name, f"{type1}/{type2}"]
        if len(context_names) == 1:
            location.append(context_names[0])
        raise InconsistentConfiguration(message, location=location)

    def _initialize_contexts(self):
        self.required_contexts = set()
        self.allowed_contexts = set()
        self.denied_contexts = set()
        self.contexts_specifications = {}

    def _get_package(self):  # pragma: no cover
        """
        Get package of the desired command.

        If package is not installed, returns None.

        :return: self package
        """
        importlib.reload(pkg_resources)
        for package in list(pkg_resources.working_set):
            if package.key == self.name:
                return package
        return None
