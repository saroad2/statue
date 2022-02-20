import asyncio
import mock
import pytest
import pytest_asyncio

from statue.sources_locks_repository import SourcesLocksRepository


@pytest_asyncio.fixture
async def mock_repository_total_lock():
    with mock.patch.object(
        SourcesLocksRepository, "total_lock"
    ) as total_lock_patch:
        total_lock_patch.acquire = mock.AsyncMock()
        yield total_lock_patch


@pytest.mark.asyncio
async def test_get_source_lock_once(tmp_path, mock_repository_total_lock):
    source = tmp_path / "bla.py"
    lock = await SourcesLocksRepository.get_lock(source)

    assert isinstance(lock, asyncio.Lock)
    mock_repository_total_lock.acquire.assert_awaited_once()
    mock_repository_total_lock.release.assert_called_once()


@pytest.mark.asyncio
async def test_get_source_lock_twice(tmp_path, mock_repository_total_lock):
    source = tmp_path / "bla.py"
    lock1 = await SourcesLocksRepository.get_lock(source)
    lock2 = await SourcesLocksRepository.get_lock(source)

    assert isinstance(lock1, asyncio.Lock)
    assert isinstance(lock2, asyncio.Lock)
    assert lock1 is lock2
    assert mock_repository_total_lock.acquire.await_count == 2
    assert mock_repository_total_lock.acquire.await_args_list == [mock.call(), mock.call()]
    assert mock_repository_total_lock.release.call_count == 2
    assert mock_repository_total_lock.release.call_args_list == [mock.call(), mock.call()]


@pytest.mark.asyncio
async def test_get_source_lock_on_two_files(tmp_path, mock_repository_total_lock):
    source1, source2 = tmp_path / "bla1.py", tmp_path / "bla2.py"
    lock1 = await SourcesLocksRepository.get_lock(source1)
    lock2 = await SourcesLocksRepository.get_lock(source2)

    assert isinstance(lock1, asyncio.Lock)
    assert isinstance(lock2, asyncio.Lock)
    assert lock1 is not lock2
    assert mock_repository_total_lock.acquire.await_count == 2
    assert mock_repository_total_lock.acquire.await_args_list == [mock.call(), mock.call()]
    assert mock_repository_total_lock.release.call_count == 2
    assert mock_repository_total_lock.release.call_args_list == [mock.call(), mock.call()]
