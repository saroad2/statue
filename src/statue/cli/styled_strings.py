"""Transforming plane strings into styled ones."""
import click


def source_style(source):
    """
    Styling function to emphasise sources paths.

    :param source: The source name to style
    :return: Styles source
    :rtype: str
    """
    return click.style(source, fg="cyan")


def name_style(name):
    """
    Styling function to emphasise names.

    :param name: The name to style
    :return: Styled name
    :rtype: str
    """
    return click.style(name, fg="magenta")


def bullet_style(bullet_name):
    """
    Styling function to emphasise bullet names.

    :param bullet_name: The name to style
    :return: Styled bullet name
    :rtype: str
    """
    return click.style(bullet_name, fg="yellow")


def success_style(success_string):
    """
    Styling function to emphasise bullet names.

    :param success_string: The string to style
    :return: Styled success string
    :rtype: str
    """
    return click.style(success_string, fg="green")


def failure_style(failure_string):
    """
    Styling function to emphasise bullet names.

    :param failure_string: The string to style
    :return: Styled failure string
    :rtype: str
    """
    return click.style(failure_string, fg="red")
