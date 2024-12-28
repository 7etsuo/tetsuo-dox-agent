"""
Implements the logic for each node in the message processing graph.

Dependencies:
    - json
    - typing
    - collections.defaultdict
    - langchain_core.messages
    - langgraph.prebuilt.ToolInvocation
    - dox_agent.chains: Contains first_responder, revisor, and parser
    - dox_agent.tools.search: SearchTool for TavilySearch

Functions:
    draft_node(state: List[BaseMessage]) -> List[BaseMessage]
    execute_tools_node(state: List[BaseMessage]) -> List[BaseMessage]
    revise_node(state: List[BaseMessage]) -> List[BaseMessage]
"""

import json
from typing import List
from collections import defaultdict
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langgraph.prebuilt import ToolInvocation
from dox_agent.chains import first_responder, revisor, parser
from dox_agent.tools.search import SearchTool

search_tool = SearchTool()


def draft_node(state: List[BaseMessage]) -> List[BaseMessage]:
    """
    Generate initial draft from user input.

    Args:
        state: List of messages or a string representing user's query

    Returns:
        A list of BaseMessage representing the next step in the chain.
    """
    if isinstance(state, str):
        messages = [HumanMessage(content=state)]
    elif isinstance(state, list):
        if not state:
            raise ValueError("Empty state received")
        if isinstance(state[-1], str):
            messages = [HumanMessage(content=state[-1])]
        else:
            messages = state
    else:
        raise ValueError(f"Unexpected state type: {type(state)}")

    return first_responder.invoke({"messages": messages})


def execute_tools_node(state: List[BaseMessage]) -> List[BaseMessage]:
    """
    Extract search queries from the previous AIMessage, invoke the search tool, 
    and return ToolMessage objects containing JSON results.

    Args:
        state: List of messages, with the last AIMessage containing search queries

    Returns:
        A list of ToolMessage objects with the aggregated search results in JSON.
    """
    tool_invocation: AIMessage = state[-1]
    parsed_tool_calls = parser.invoke(tool_invocation)

    ids = []
    tool_invocations = []

    for parsed_call in parsed_tool_calls:
        for query in parsed_call["args"]["search_queries"]:
            tool_invocations.append(
                ToolInvocation(
                    tool="tavily_search_results_json",
                    tool_input=query,
                )
            )
            ids.append(parsed_call["id"])

    outputs = [
        search_tool.execute(invocation.tool_input)
        for invocation in tool_invocations
    ]

    outputs_map = defaultdict(dict)
    for id_, output, invocation in zip(ids, outputs, tool_invocations):
        outputs_map[id_][invocation.tool_input] = output

    return [
        ToolMessage(
            content=json.dumps(query_outputs),
            tool_call_id=id_
        )
        for id_, query_outputs in outputs_map.items()
    ]


def revise_node(state: List[BaseMessage]) -> List[BaseMessage]:
    """
    Revise the generated answer by incorporating newly found search results.

    Args:
        state: List of messages containing search results and prior answer

    Returns:
        Revised answer messages returned by the revisor chain.
    """
    return revisor.invoke({"messages": state})
