"""
Type definitions for the dox-agent system.

Defines aliases for commonly used type hints throughout the codebase.

    - SearchResult: A dictionary of search result data
    - ToolResponse: A dictionary for tool response data
    - MessageState: A list of BaseMessage for chaining
"""

from typing import TypeAlias, Dict, Any, List
from langchain_core.messages import BaseMessage

SearchResult: TypeAlias = Dict[str, Any]
ToolResponse: TypeAlias = Dict[str, Any]
MessageState: TypeAlias = List[BaseMessage]
