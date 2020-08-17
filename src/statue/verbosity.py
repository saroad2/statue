"""Verbosity related constants and methods."""
SILENT = "silent"
VERBOSE = "verbose"
NORMAL = "normal"

VERBOSITIES = [NORMAL, SILENT, VERBOSE]
DEFAULT_VERBOSITY = NORMAL


def is_silent(verbosity: str) -> bool:
    """
    Validates if verbosity is silent.

    :param verbosity: String. verbosity value
    :return: Boolean. is verbosity silent
    """
    return verbosity == SILENT


def is_verbose(verbosity: str) -> bool:
    """
    Validates if verbosity is verbose.

    :param verbosity: String. verbosity value
    :return: Boolean. is verbosity verbose
    """
    return verbosity == VERBOSE
