"""Prompt repository module."""
from dataclasses import dataclass, field
from typing import Any

from langchain_core.prompts.base import BasePromptTemplate
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


_hub = PromptHub(use_async=True)


async def get_extraction_prompt(
    persona: str,
    intents: str,
    schema: dict,
    language: str = "English",
) -> str:
    """Extract certain data from text based on given `schema`.

    Args:
        persona (str): user persona description.
        intents (str): list of intents for intent detection.
        schema (str): schema for entity extraction.
        language (str): language of the response. Defaults to "English".

    Returns:
        str: prompt template.
    """
    prompt = await _hub.get_prompt("extraction")
    if isinstance(prompt, BasePromptTemplate):
        return prompt.content.format(
            persona=persona,
            intents=intents,
            schema=schema,
            language=language,
        )
    return prompt


async def get_text_to_sql_prompt(
    dialect: str,
    top_k: str,
    question: str,
) -> str:
    """Text-to-SQL prompt agent.

    Args:
        dialect (str): database dialect.
        top_k (str): max number of results as limit statement in SQL.
        question (str): contextual transformed user question.
    """
    prompt: BasePromptTemplate = await _hub.get_prompt("text-to-sql")
    if isinstance(prompt, BasePromptTemplate):
        return prompt.format(
            dialect=dialect,
            top_k=top_k,
            question=question,
        )
    return prompt
