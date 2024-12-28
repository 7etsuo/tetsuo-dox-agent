"""
Provides functionality to build and compile the message processing graph.

Dependencies:
    - langchain_core.messages: For BaseMessage, ToolMessage
    - langgraph.graph: The main graph framework
    - dox_agent.config.settings: For configuration
    - dox_agent.graph.nodes: Graph nodes for drafting, executing tools, and revising

Usage:
    from dox_agent.graph.builder import create_graph
    graph = create_graph()
    result = graph.invoke("Your question here")
"""

from typing import List
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph
from dox_agent.config.settings import settings
from .nodes import draft_node, execute_tools_node, revise_node


def create_event_loop(max_iterations: int):
    """
    Generates an event loop callback function that determines
    transitions between graph nodes.

    Args:
        max_iterations: Maximum number of times tools can be invoked

    Returns:
        A function that takes state (list of BaseMessage) and returns the next node name.
    """
    def event_loop(state: List[BaseMessage]) -> str:
        count_tool_visits = sum(isinstance(item, ToolMessage)
                                for item in state)
        if count_tool_visits > max_iterations:
            return END
        return "execute_tools"
    return event_loop


def create_graph(max_iterations: int = settings.MAX_ITERATIONS) -> MessageGraph:
    """
    Constructs and compiles the message graph for question-answering.

    Args:
        max_iterations: Maximum number of tool invocations

    Returns:
        A compiled MessageGraph object with the defined nodes and transitions.
    """
    builder = MessageGraph()

    builder.add_node("draft", draft_node)
    builder.add_node("execute_tools", execute_tools_node)
    builder.add_node("revise", revise_node)

    builder.add_edge("draft", "execute_tools")
    builder.add_edge("execute_tools", "revise")

    builder.add_conditional_edges(
        "revise",
        create_event_loop(max_iterations)
    )

    builder.set_entry_point("draft")

    return builder.compile()
