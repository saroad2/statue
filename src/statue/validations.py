"""Validation method for arguments."""


def validate(args):
    """
    Validate given args.

    :param args: :class:`Namespace` of arguments.
    :raise ValueError: When encountering an error.
    """
    if not args.settings.exists():
        raise ValueError(f'Settings file "{args.settings}" doesn\'t exists')
    non_existing_input_paths = [
        '"' + str(path) + '"' for path in args.input if not path.exists()
    ]
    if len(non_existing_input_paths) != 0:
        joined_paths = ", ".join(non_existing_input_paths)
        raise ValueError(f"The following input paths doesn't exists: {joined_paths}")
