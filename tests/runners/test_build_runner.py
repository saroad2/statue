from statue.runner import (
    AsynchronousEvaluationRunner,
    RunnerMode,
    SynchronousEvaluationRunner,
    build_runner,
)


def test_runner_mode_enum():
    assert RunnerMode.SYNC.name == "SYNC"
    assert RunnerMode.ASYNC.name == "ASYNC"
    assert RunnerMode.SYNC.value != RunnerMode.ASYNC.value
    assert set(RunnerMode) == {RunnerMode.SYNC, RunnerMode.ASYNC}


def test_build_sync_evaluation_runner():
    runner = build_runner(RunnerMode.SYNC.name)

    assert isinstance(runner, SynchronousEvaluationRunner)


def test_build_async_evaluation_runner(event_loop):
    runner = build_runner(RunnerMode.ASYNC.name)

    assert isinstance(runner, AsynchronousEvaluationRunner)
