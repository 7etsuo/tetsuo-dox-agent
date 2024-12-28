"""
Tool for executing TavilySearch queries.

Dependencies:
    - langchain_community.tools.tavily_search: Provides the TavilySearchResults tool
    - langchain_community.utilities.tavily_search: API wrapper for TavilySearch
    - dox_agent.config.settings: For app settings
"""

from typing import List, Dict, Any
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from dox_agent.config.settings import settings


class SearchTool:
    """
    Encapsulates TavilySearch functionality for external resource lookups.

    Usage:
        search_tool = SearchTool()
        results = search_tool.execute("query string")

    Methods:
        execute(query: str) -> List[Dict[str, Any]]:
            Performs the search and returns list of result items.
    """

    def __init__(self):
        self.search = TavilySearchAPIWrapper(
            tavily_api_key=settings.TAVILY_API_KEY
        )
        self.tavily_tool = TavilySearchResults(
            api_wrapper=self.search,
            max_results=settings.MAX_RESULTS
        )

    def execute(self, query: str) -> List[Dict[str, Any]]:
        return self.tavily_tool.invoke(query)
