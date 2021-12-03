# noqa: D100
# pylint: disable=missing-module-docstring
import importlib
import os
import subprocess  # nosec
import sys
from dataclasses import dataclass, field
from typing import List, Optional

import pkg_resources

from statue.exceptions import CommandExecutionError
from statue.verbosity import DEFAULT_VERBOSITY, is_silent, is_verbose


@dataclass
class Command:
    """
    Data class representing a command to run in order to evaluate the code.

    :param name: The name of the command to run.
    :param args: A list of arguments for the command.
    :param help: Help string
    :param version: One can specify a specific version of the command to use
    """

    name: str
    help: str
    args: List[str] = field(default_factory=list)
    version: Optional[str] = field(default=None)

    @property
    def install_name(self):
        if self.version is None:
            return self.name
        return f"{self.name}=={self.version}"

    @property
    def installed_version(self) -> Optional[str]:
        package = self._get_package()
        if package is None:
            return None
        return package.version

    def installed(self) -> bool:
        """
        Is this command installed.

        :return: Either the command is installed or not
        :rtype: bool
        """
        package = self._get_package()
        return package is not None

    def installed_correctly(self) -> bool:
        return self.installed() and self.installed_version_match()

    def install(self, verbosity: str = DEFAULT_VERBOSITY, latest: bool = False) -> None:
        """
        Install command using pip.

        :param verbosity: Verbosity level.
        :param latest: Install the latest version of package.
        :type verbosity: str
        """
        if self.installed():
            return
        if not is_silent(verbosity):
            print(f"Installing {self.install_name}")
        subprocess.run(  # nosec
            [sys.executable, "-m", "pip", "install", (self.name if latest else self.install_name)],
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
        if self.installed():
            return
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
        Install command using pip.

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
        if not self.installed():
            self.install()
        if self.installed_version_match():
            return
        self.uninstall(verbosity=verbosity)
        self.install(verbosity=verbosity)

    def execute(  # pylint: disable=too-many-arguments
        self,
        source: str,
        verbosity: str = DEFAULT_VERBOSITY,
    ) -> int:
        """
        Execute the command.

        :param source: source files to check.
        :type: str
        :param verbosity: Indicates the verbosity of the prints to console.
        :type verbosity: str
        :return: Exit code of the command
        :rtype: int
        """
        args = [self.name, source, *self.args]
        if is_verbose(verbosity):
            print(f"Running the following command: \"{' '.join(args)}\"")
        return self._run_subprocess(args, verbosity)

    def installed_version_match(self):
        return self.installed_version == self.version

    def _run_subprocess(self, args: List[str], verbosity: str) -> int:
        try:
            return subprocess.run(  # nosec
                args,
                env=os.environ,
                check=False,
                capture_output=is_silent(verbosity),
            ).returncode
        except FileNotFoundError as error:
            raise CommandExecutionError(self.name) from error

    def _get_package(self):
        """
        Get package of the desired command
        If package is not installed, returns None.

        :return: self package
        """
        importlib.reload(pkg_resources)
        for package in pkg_resources.working_set:
            if package.key == self.name:
                return package
        return None
