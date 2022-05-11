# Quick Start

## Installation
In order to install *Statue*, simply run:

    pip install statue

You can validate statue has been installed successfully by running:

    statue --version

Which will print:

    statue, version {{ version  }}

## Initialize *Statue*

In order for *Statue* to work correctly, you need to initialize *statue.toml* configuration file.
This is simply done using the command:

    statue config init

Just follow the instructions, and your *Statue* configuration file will be ready!
You can see which commands have been set in your configuration using the command:

    statue config show-tree

If you want to look at your configuration file as plain text, you can alternatively use:

    statue config show

## Run!
Now that your configuration file is ready, simply run:

    statue run
   
And all the formatters and linters defined in the configuration will run on your codebase.

## What's Next?
- Learn how to use `statue run` in various ways to improve efficiency
- Learn how to use contexts in order to run your formatters and linters with different arguments