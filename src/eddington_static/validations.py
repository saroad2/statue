def validate(args):
    if not args.settings.exists():
        raise ValueError(f'Settings file "{args.settings}" doesn\'t exists')
    non_existing_input_paths = [
        '"' + str(path) + '"' for path in args.input if not path.exists()
    ]
    if len(non_existing_input_paths):
        joined_paths = ", ".join(non_existing_input_paths)
        raise ValueError(f"The following input paths doesn't exists: {joined_paths}")
