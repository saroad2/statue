"""Singleton for storing sources locks for async commands execution."""
import asyncio
from pathlib import Path
from typing import Dict


class SourcesLocksRepository:  # pylint: disable=too-few-public-methods
    """
    Singleton for storing sources locks.

    This is used for async commands executions.
    """

    total_lock: asyncio.Lock = asyncio.Lock()
    locks_dict: Dict[Path, asyncio.Lock] = {}

    @classmethod
    async def get_lock(cls, source: Path) -> asyncio.Lock:
        """
        Get lock of a specific source.

        First check if the source has an existing lock. For this check
        we must lock the entire repository using the total_lock.
        If lock is not existing, creating it.

        After that, returning the lock.

        :param source: The source to get its lock
        :type source: Path
        :return: The source's lock
        :rtype: asyncio.Lock
        """
        await cls.total_lock.acquire()
        if source not in cls.locks_dict:
            cls.locks_dict[source] = asyncio.Lock()
        cls.total_lock.release()
        return cls.locks_dict[source]
