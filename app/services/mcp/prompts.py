"""MCP Prompts."""

from langchain_core.prompts.base import BasePromptTemplate

from app.repository.prompt import PromptHub

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


async def get_pfa_planner_prompt(
    budget_rules: str,
    current_spending: str,
    transaction_data: str,
    spending_threshold: str,
) -> str:
    """PFA planner prompt agent.

    Args:
        budget_rules (str): Rules for budgeting.
        current_spending (str): Current monthly spending.
        transaction_data (str): Transaction data to analyze.
        spending_threshold (str): Spending threshold.
    """
    prompt: BasePromptTemplate = await _hub.get_prompt("pfa-planner")
    if isinstance(prompt, BasePromptTemplate):
        return prompt.format(
            budget_rules=budget_rules,
            current_spending=current_spending,
            transaction_data=transaction_data,
            spending_threshold=spending_threshold,
        )
    return prompt
