"""
Provides chain configurations for handling the primary prompts.

Dependencies:
    - langchain_core: For parser utilities
    - langchain_openai: For ChatOpenAI
    - dox_agent.config.settings: For app settings
    - dox_agent.models.answer: For Pydantic-based question-answer models
    - dox_agent.prompts: For prompt templates

Usage:
    Imported by graph nodes to create first-responder and revisor chain objects.
"""

from langchain_core.output_parsers.openai_tools import (
    PydanticToolsParser,
    JsonOutputToolsParser,
)
from langchain_openai import ChatOpenAI
from dox_agent.config.settings import settings
from dox_agent.models.answer import AnswerQuestion, ReviseAnswer
from dox_agent.prompts import first_prompt, revise_prompt

llm = ChatOpenAI(
    api_key=settings.OPENAI_API_KEY,
    model=settings.MODEL_NAME
)

parser = JsonOutputToolsParser(return_id=True)
validator = PydanticToolsParser(tools=[AnswerQuestion])

first_responder = first_prompt | llm.bind_tools(
    tools=[AnswerQuestion],
    tool_choice="AnswerQuestion"
)

revisor = revise_prompt | llm.bind_tools(
    tools=[ReviseAnswer],
    tool_choice="ReviseAnswer"
)
