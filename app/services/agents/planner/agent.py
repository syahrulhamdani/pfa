from dataclasses import dataclass, field

from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import google_search
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.prompts.base import BasePromptTemplate
from langsmith.integrations.otel import configure
from loguru import logger as _LOGGER

from app.services.agents import planner
from app.repository.prompt import PromptHub

configure()


@dataclass
class PlannerAgent:
    """Planner agent."""
    name: str = "planner_agent"
    model: str = "gemini-2.5-flash"
    description: str = planner.__doc__
    prompt_name: str = "pfa-planner"
    tools: list = field(default_factory=lambda: [google_search])

    def __post_init__(self) -> None:
        self.prompt_hub = PromptHub(use_async=False)

    def _get_instruction(self) -> str:
        prompt: PromptTemplate | ChatPromptTemplate = self.prompt_hub.get_prompt(
            self.prompt_name
        )
        if isinstance(prompt, PromptTemplate):
            _LOGGER.info("Returning prompt template")
            return prompt.template

        if isinstance(prompt, ChatPromptTemplate):
            _LOGGER.info("Returning chat prompt template.")
            instruction: ChatPromptTemplate = prompt.invoke(
                {"spending_threshold": "500,000 IDR"}
            )
            err = instruction.messages[0]
            print(err, type(err))
            return instruction.messages[0].content

        _LOGGER.info("Returning prompt as is.")
        return prompt

    @property
    def agent(self) -> Agent:
        """Agent object."""
        if not hasattr(self, "_agent"):
            agent =  Agent(
                model=self.model,
                name=self.name,
                description=self.description,
                instruction=self._get_instruction(),
                tools=self.tools,
            )
            setattr(self, "_agent", agent)
        return getattr(self, "_agent")


planner_agent = PlannerAgent()
root_agent = planner_agent.agent
