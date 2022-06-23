from tests.constants import COMMAND1, COMMAND_HELP_STRING1
from tests.util import dummy_context, dummy_full_command_builder


def test_command_builder_remove_non_existing_context():
    command_builder = dummy_full_command_builder(
        name=COMMAND1, help_string=COMMAND_HELP_STRING1
    )
    allowed_contexts = command_builder.allowed_contexts
    denied_contexts = command_builder.denied_contexts
    required_contexts = command_builder.required_contexts
    contexts_specifications = command_builder.contexts_specifications

    command_builder.remove_context(dummy_context())

    assert command_builder.allowed_contexts == allowed_contexts
    assert command_builder.denied_contexts == denied_contexts
    assert command_builder.required_contexts == required_contexts
    assert command_builder.contexts_specifications == contexts_specifications


def test_command_builder_remove_allowed_context():
    command_builder = dummy_full_command_builder(
        name=COMMAND1, help_string=COMMAND_HELP_STRING1
    )
    context1, context2 = command_builder.allowed_contexts
    denied_contexts = command_builder.denied_contexts
    required_contexts = command_builder.required_contexts
    contexts_specifications = command_builder.contexts_specifications

    command_builder.remove_context(context1)

    assert command_builder.allowed_contexts == {context2}
    assert command_builder.denied_contexts == denied_contexts
    assert command_builder.required_contexts == required_contexts
    assert command_builder.contexts_specifications == contexts_specifications


def test_command_builder_remove_denied_context():
    command_builder = dummy_full_command_builder(
        name=COMMAND1, help_string=COMMAND_HELP_STRING1
    )
    allowed_contexts = command_builder.allowed_contexts
    context1, context2 = command_builder.denied_contexts
    required_contexts = command_builder.required_contexts
    contexts_specifications = command_builder.contexts_specifications

    command_builder.remove_context(context1)

    assert command_builder.allowed_contexts == allowed_contexts
    assert command_builder.denied_contexts == {context2}
    assert command_builder.required_contexts == required_contexts
    assert command_builder.contexts_specifications == contexts_specifications


def test_command_builder_remove_required_context():
    command_builder = dummy_full_command_builder(
        name=COMMAND1, help_string=COMMAND_HELP_STRING1
    )
    allowed_contexts = command_builder.allowed_contexts
    denied_contexts = command_builder.denied_contexts
    context1, context2 = command_builder.required_contexts
    contexts_specifications = command_builder.contexts_specifications

    command_builder.remove_context(context1)

    assert command_builder.allowed_contexts == allowed_contexts
    assert command_builder.denied_contexts == denied_contexts
    assert command_builder.required_contexts == {context2}
    assert command_builder.contexts_specifications == contexts_specifications


def test_command_builder_remove_specified_context():
    command_builder = dummy_full_command_builder(
        name=COMMAND1, help_string=COMMAND_HELP_STRING1
    )
    allowed_contexts = command_builder.allowed_contexts
    denied_contexts = command_builder.denied_contexts
    required_contexts = command_builder.required_contexts
    contexts_specifications = command_builder.contexts_specifications
    context1, context2 = command_builder.specified_contexts

    command_builder.remove_context(context1)

    assert command_builder.allowed_contexts == allowed_contexts
    assert command_builder.denied_contexts == denied_contexts
    assert command_builder.required_contexts == required_contexts
    assert command_builder.contexts_specifications == {
        context2: contexts_specifications[context2]
    }
