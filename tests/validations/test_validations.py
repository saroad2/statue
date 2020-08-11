from argparse import Namespace

import pytest

from statue.validations import validate


def test_validation_passes(existing_settings, existing_input1, existing_input2):
    args = Namespace(
        commands_file=existing_settings, input=[existing_input1, existing_input2]
    )
    validate(args)


def test_setting_doesnt_exists(
    non_existing_settings, existing_input1, existing_input2, existing_input3
):
    args = Namespace(
        commands_file=non_existing_settings,
        input=[existing_input1, existing_input2, existing_input3],
    )
    with pytest.raises(ValueError) as exception:
        validate(args)

    assert str(exception.value) == (
        f'Settings file "{non_existing_settings}" doesn\'t exists'
    )


def test_one_input_file_doesnt_exists(
    existing_settings, existing_input1, existing_input2, non_existing_input_file1
):
    args = Namespace(
        commands_file=existing_settings,
        input=[existing_input1, non_existing_input_file1, existing_input2],
    )
    with pytest.raises(ValueError) as exception:
        validate(args)

    assert str(exception.value) == (
        f'The following input paths don\'t exist: "{non_existing_input_file1}"'
    )


def test_two_input_files_doesnt_exists(
    existing_settings,
    existing_input1,
    non_existing_input_file1,
    non_existing_input_file2,
):
    args = Namespace(
        commands_file=existing_settings,
        input=[existing_input1, non_existing_input_file1, non_existing_input_file2],
    )
    with pytest.raises(ValueError) as exception:
        validate(args)

    assert str(exception.value) == (
        "The following input paths don't exist: "
        f'"{non_existing_input_file1}", "{non_existing_input_file2}"'
    )
