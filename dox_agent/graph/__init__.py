"""
Graph processing package for dox-agent.

This package implements the core question-answering workflow using a directed graph
architecture powered by LangGraph. It manages the flow of messages between different
processing nodes to generate and refine answers.

Components:
    - builder: Graph construction and compilation
    - nodes: Individual processing nodes for drafting, tool execution, and revision

Graph Flow:
    1. Draft Node: Creates initial answer
    2. Execute Tools Node: Performs external searches
    3. Revise Node: Refines answer based on search results

Usage:
    from dox_agent.graph.builder import create_graph
    graph = create_graph()
    result = graph.invoke("Your question here")
"""

from .builder import create_graph
from .nodes import draft_node, execute_tools_node, revise_node

__all__ = ["create_graph", "draft_node", "execute_tools_node", "revise_node"]
