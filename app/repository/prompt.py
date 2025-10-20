"""Prompt repository module."""
from dataclasses import dataclass, field
from typing import Any

from langsmith import AsyncClient, Client
from langsmith.schemas import ListPromptsResponse
from loguru import logger as _LOGGER

from app.core.config import config as c


@dataclass
class PromptHub:
    """Prompt repository instance."""
    langsmith_project: str = field(default=c.LANGSMITH_PROJECT)
    use_async: bool = field(default_factory=bool)

    @property
    def client(self) -> AsyncClient | Client:
        """Langsmith client."""
        if not hasattr(self, "_client"):
            client = (
                AsyncClient(api_key=c.LANGSMITH_API_KEY)
                if self.use_async else Client(api_key=c.LANGSMITH_API_KEY)
            )
            setattr(self, "_client", client)
        return getattr(self, "_client")

    async def list_prompts(self, is_public: bool = False) -> ListPromptsResponse:
        """List all available prompts in Langsmith, filtered by `is_public`.

        Args:
            is_public (bool, optional): Filter by `is_public`. Defaults to False,
                which will fetch from private repo.

        Returns:
            ListPromptsResponse: list of prompts.
        """
        prompts = await self.client.list_prompts(is_public=is_public)
        return prompts

    async def get_prompt(self, prompt_id: str) -> Any:
        """Get a prompt from langsmith by prompt name.

        Args:
            prompt_id (str): prompt name.

        Returns:
            Prompt: prompt instance.
        """
        prompt = await self.client.pull_prompt(prompt_id)
        return prompt
