"""Repository layer for Google Cloud Storage."""
import asyncio
from dataclasses import dataclass

from google.cloud import storage
from loguru import logger as _LOGGER

from app.core.config import config as c


@dataclass
class Storage:
    """Google Cloud Storage interface class."""
    bucket_id: str

    @property
    def bucket(self) -> storage.client.Bucket:
        """Google Cloud Storage bucket."""
        if not hasattr(self, "_bucket"):
            client = storage.Client()
            setattr(self, "_bucket", client.get_bucket(self.bucket_id))
        return getattr(self, "_bucket")

    def get(self, blob_name: str) -> str:
        """Get a blob from Google Cloud Storage.

        Args:
            blob_name (str): blob name.

        Returns:
            str: blob content.
        """
        _LOGGER.info("Downloading blob: {blob_name}")
        blob = self.bucket.blob(blob_name)
        content = blob.download_as_bytes().decode("utf-8")
        _LOGGER.info("Successfully downloaded blob: {blob_name}")
        return content

    def get_all_blobs(self, match_glob: str) -> list[storage.blob.Blob]:
        """Get all object blobs."""
        blobs = []
        for blob in self.bucket.get_blob(match_glob=match_glob):
            if "pdf" in blob.content_type:
                blobs.append(blob)
                continue

            content = blob.download_as_bytes().decode("utf-8")
            blobs.append(content)
        return blobs


_gcs = Storage(bucket_id=c.GCS_BUCKET_ID)
