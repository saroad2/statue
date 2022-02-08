from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli.string_util import title_string


def case_empty_title():
    original_string = ""
    title = "\n"
    kwargs = {}

    return original_string, title, kwargs


def case_one_char_title():
    original_string = "a"
    title = "A\n="
    kwargs = {}

    return original_string, title, kwargs


def case_one_word_title():
    original_string = "awesome"
    title = "Awesome\n======="
    kwargs = {}

    return original_string, title, kwargs


def case_two_words_title():
    original_string = "awesome title"
    title = "Awesome Title\n============="
    kwargs = {}

    return original_string, title, kwargs


def case_different_underline():
    original_string = "awesome title"
    title = "Awesome Title\n-------------"
    kwargs = dict(underline="-")

    return original_string, title, kwargs


def case_no_transform():
    original_string = "awesome title"
    title = "awesome title\n============="
    kwargs = dict(transform=False)

    return original_string, title, kwargs


@parametrize_with_cases(
    argnames=["original_string", "title", "kwargs"], cases=THIS_MODULE
)
def test_print_title(original_string, title, kwargs):
    assert title_string(original_string, **kwargs) == title
