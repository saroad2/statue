"""Validation method for arguments."""


def validate(args):
    """
    Validate given args.

    :param args: :class:`Namespace` of arguments.
    :raise ValueError: When encountering an error.
    """
    if not args.commands_file.exists():
        raise ValueError(f'Settings file "{args.commands_file}" doesn\'t exists')
    non_existing_input_paths = [
        '"' + str(path) + '"' for path in args.input if not path.exists()
    ]
    if len(non_existing_input_paths) != 0:
        joined_paths = ", ".join(non_existing_input_paths)
        raise ValueError(f"The following input paths don't exist: {joined_paths}")
