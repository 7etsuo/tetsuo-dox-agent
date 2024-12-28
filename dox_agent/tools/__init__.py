"""
Tools package for dox-agent.

This package provides various utility tools and external service integrations
used by the question-answering system.

Available Tools:
    - SearchTool: Interface for TavilySearch integration, providing web search capabilities

Usage:
    from dox_agent.tools.search import SearchTool
"""

from .search import SearchTool

__all__ = ["SearchTool"]
