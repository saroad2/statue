import click
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli.string_util import boxed_string


def case_empty_text():
    original_string = ""
    title = "####\n#  #\n####"
    kwargs = {}

    return original_string, title, kwargs


def case_one_char_text():
    original_string = "a"
    title = "#####\n# A #\n#####"
    kwargs = {}

    return original_string, title, kwargs


def case_one_word_text():
    original_string = "awesome"
    title = "###########\n# Awesome #\n###########"
    kwargs = {}

    return original_string, title, kwargs


def case_two_words_text():
    original_string = "awesome string"
    title = "##################\n# Awesome String #\n##################"
    kwargs = {}

    return original_string, title, kwargs


def case_different_border():
    original_string = "awesome string"
    title = "$$$$$$$$$$$$$$$$$$\n$ Awesome String $\n$$$$$$$$$$$$$$$$$$"
    kwargs = dict(border="$")

    return original_string, title, kwargs


def case_styled_string():
    original_string = click.style("awesome", fg="green")
    title = f"###########\n# {click.style('Awesome', fg='green')} #\n###########"
    kwargs = {}

    return original_string, title, kwargs


@parametrize_with_cases(
    argnames=["original_string", "title", "kwargs"], cases=THIS_MODULE
)
def test_print_boxed(original_string, title, kwargs):
    assert boxed_string(original_string, **kwargs) == title
