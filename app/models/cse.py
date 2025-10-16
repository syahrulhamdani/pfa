"""Custom Search Engine result data model."""

from pydantic import BaseModel, Field


class CSEItem(BaseModel):
    """Custom Search Engine item result."""
    title: str = Field(default_factory=str)
    link: str = Field(default_factory=str)
    content: str = Field(default_factory=str)
    metadata: dict = Field(default_factory=dict)


class CSEResults(BaseModel):
    """Custom Search Engine list of items."""
    results: list[CSEItem]
