"""
Centralized application settings using pydantic_settings.

Environment variables:
    - OPENAI_API_KEY: API key for OpenAI
    - TAVILY_API_KEY: API key for TavilySearch
    - LANGCHAIN_API_KEY: Optional key for LangChain
    - LANGCHAIN_TRACING_V2: Optional boolean for LangChain tracing
    - LANGCHAIN_PROJECT: Optional project identifier for LangChain
    - MAX_ITERATIONS: Maximum iteration count for tool usage
    - MODEL_NAME: Default model name
    - MAX_RESULTS: Maximum results for searches

Usage:
    from dox_agent.config.settings import settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_TRACING_V2: Optional[bool] = None
    LANGCHAIN_PROJECT: Optional[str] = None
    MAX_ITERATIONS: int = 3
    MODEL_NAME: str = "gpt-4-turbo-preview"
    MAX_RESULTS: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
