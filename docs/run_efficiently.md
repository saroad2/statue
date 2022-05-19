# Run Efficiently

## Starting Simple
The simplest way you can run *Statue* is to use the following command:

    statue run

This will run all formatters and linters in your configuration on your codebase. This will result in two ways:

If the run finished successfully, the following will be printed:

    Statue finished successfully after 24.66 seconds!

Otherwise, all the failing commands will be printed with the respective source they ran on. For example:

    src\statue:
            black, pydocstyle, pylint
    tests:
            black, flake8


If you scroll up your terminal you'll see the output of each command, including those who failed.
Now you can fix the errors and rerun `statue run`.

## Know Your History

By running:

    statue history list

You can see your latest run history. By default, *Statue* will save the last {{ history_size() }} runs.
The history output will look like this:

    1) 05/12/2022, 09:00:23 - Success (16/16 successful, 20.00 seconds)
    2) 05/12/2022, 08:59:55 - Failure (14/16 successful, 20.24 seconds)
    3) 05/12/2022, 08:54:53 - Success (16/16 successful, 24.66 seconds)
    4) 05/11/2022, 15:43:30 - Success (16/16 successful, 40.94 seconds)
    5) 05/11/2022, 15:42:58 - Success (3/3 successful, 24.73 seconds)
    6) 05/11/2022, 15:38:52 - Failure (13/16 successful, 19.74 seconds)
    7) 05/11/2022, 15:38:26 - Success (9/9 successful, 2.30 seconds)

In order to see the exact commands that ran in a given evaluation, use the `statue history show` command.
For example, if you want to take a look at evaluation 6 above, you can run:

    statue history show -n 6

And an output like the following will be printed:

    05/11/2022, 15:38:52 - Failure (13/16 successful, 19.74 seconds)
    setup.py (1.08 seconds):
            black - Success (0.26 seconds)
            flake8 - Success (0.35 seconds)
            isort - Success (0.46 seconds)
    src\statue (15.58 seconds):
            bandit - Success (1.47 seconds)
            black - Success (0.25 seconds)
            darglint - Failure (1.49 seconds)
            flake8 - Failure (1.18 seconds)
            isort - Success (0.28 seconds)
            mypy - Success (0.67 seconds)
            pydocstyle - Success (0.87 seconds)
            pylint - Failure (9.35 seconds)
    tests (19.72 seconds):
            black - Success (0.39 seconds)
            flake8 - Success (2.80 seconds)
            isort - Success (0.40 seconds)
            mypy - Success (0.90 seconds)
            pylint - Success (15.21 seconds)

## Do it again!

After running *Statue* multiple times with multiple contexts, you might want to re-run the last failing evaluation.
You can do so by running:

    statue run -f

This command will search for the last failing evaluation (evaluation 2 in the example above) and re-run it. Pay
attention that using `-f` flag will re-run the entire evaluation, including commands that finished successfully.
If you want to only run the failed commands from the last failed evaluation, run:

    statue run -fo

If you want to re-run a specific evaluation from history, You can do so by using the `-p` flag.
For example, if you want to re-run evaluation 6 from before, you can do so by running:

    statue run -p 6

If you want to re-run only the failed commands from evaluation 6, run:

    statue run -p 6 -f

Or:

    statue run -p 6 -fo


## What's Next?
- Learn how to use [contexts](contexts.md) in order to specify the way you want
your formatters and linters to run