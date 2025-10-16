"""Base repository."""

class BaseRepository:
    """Base repository class."""
    async def aget(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError
