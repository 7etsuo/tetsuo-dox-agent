"""
Command Line Interface for the dox-agent system.

This module provides the command-line interface for interacting with the dox-agent 
research and question-answering system. It handles configuration, user input, 
and output formatting for both interactive and file-based results.

Dependencies:
    - click: For command line argument parsing
    - dotenv: For environment variable management
    - dox_agent.config: For application settings
    - dox_agent.graph: For question processing pipeline
"""

import click
from dotenv import load_dotenv
import json
import ast
from typing import Optional, Dict, Any, Union, Tuple
from dox_agent.config.settings import settings
from dox_agent.graph.builder import create_graph


def validate_environment() -> None:
    """
    Validate that all required environment variables are properly set.

    This function checks for the presence of required API keys in the environment.
    It should be called before any operations that require external API access.

    Raises:
        ValueError: If OPENAI_API_KEY or TAVILY_API_KEY are not set in environment
    """
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    if not settings.TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY not found in environment variables")


def update_settings(max_iterations: Optional[int],
                    model: Optional[str],
                    max_results: Optional[int]) -> None:
    """
    Update application settings with command line arguments.

    Args:
        max_iterations: Maximum number of search-revise iterations to perform
        model: OpenAI model identifier to use for completions
        max_results: Maximum number of search results to return per query

    Note:
        Only updates settings that are explicitly provided (not None)
    """
    if max_iterations is not None:
        settings.MAX_ITERATIONS = max_iterations
    if model is not None:
        settings.MODEL_NAME = model
    if max_results is not None:
        settings.MAX_RESULTS = max_results


def parse_reference(ref: str) -> Dict[str, str]:
    """
    Parse a reference string that looks like a dictionary into an actual dictionary.

    Args:
        ref: String representation of a dictionary

    Returns:
        Dictionary containing the reference data
    """
    try:
        # Handle string that looks like a dictionary
        if isinstance(ref, str) and ref.strip().startswith("{"):
            return ast.literal_eval(ref)
        return {"text": str(ref)}
    except:
        return {"text": str(ref)}


def format_reference(ref: Union[Dict[str, str], str], index: int) -> str:
    """
    Format a single reference with proper citation style.

    Args:
        ref: Either a dictionary containing reference data or a string
        index: Citation number for this reference

    Returns:
        Formatted reference string
    """
    if isinstance(ref, str):
        ref_dict = parse_reference(ref)
    else:
        ref_dict = ref

    if "Author" in ref_dict:
        author = ref_dict.get("Author", "No Author")
        title = ref_dict.get("Title", "No Title")
        url = ref_dict.get("URL", "No URL")
        date = ref_dict.get("Date", "N/A")
        return f"[{index}] {author} - {title} - {url} ({date})"
    else:
        return f"[{index}] {ref_dict.get('text', str(ref))}"


def format_verbose_output(message: Any) -> str:
    """
    Format a message object for verbose output display.

    Creates a detailed string representation of a message object including:
    - Answer text
    - Reflection data (missing and superfluous information)
    - Search queries used
    - References cited

    Args:
        message: Message object containing tool calls and arguments

    Returns:
        Formatted string containing all available message details
    """
    output = []
    if hasattr(message, "tool_calls"):
        for tool_call in message.tool_calls:
            args = tool_call["args"]
            output.append("\nAnswer: " + args.get("answer", ""))

            reflection = args.get("reflection", {})
            output.append("\nReflection:")
            output.append("Missing: " + reflection.get("missing", ""))
            output.append("Superfluous: " + reflection.get("superfluous", ""))

            output.append("\nSearch Queries: " +
                          str(args.get("search_queries", [])))

            if "references" in args:
                output.append("\nReferences:")
                references = args["references"]
                for i, ref in enumerate(references, 1):
                    output.append(format_reference(ref, i))

    return "\n".join(output)


def format_standard_output(message: Any) -> Tuple[str, list[str]]:
    """
    Format a message object for standard output display.

    Args:
        message: Message object containing tool calls and arguments

    Returns:
        Tuple containing:
        - str: The answer text
        - list[str]: Formatted list of references
    """
    args = message.tool_calls[0]["args"]
    answer = args["answer"]
    references = args.get("references", [])

    formatted_refs = []
    for i, ref in enumerate(references, 1):
        formatted_refs.append(format_reference(ref, i))

    return answer, formatted_refs


def save_output_to_file(output: Dict[str, Any], filename: str) -> None:
    """
    Save the output data to a JSON file.

    Args:
        output: Dictionary containing the output data to save
        filename: Path to the output file

    Raises:
        IOError: If unable to write to the specified file
        json.JSONDecodeError: If output cannot be serialized to JSON
    """
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)


def process_and_display_output(result: list, verbose: bool, save_output: Optional[str]) -> None:
    """
    Process results and display them according to specified format.

    Handles both verbose and standard output formats, and optionally
    saves results to a file.

    Args:
        result: List of message objects containing results
        verbose: Whether to use verbose output format
        save_output: Optional file path to save results

    Side Effects:
        - Prints output to stdout
        - May write to file system if save_output is specified
    """
    if verbose:
        for message in result:
            print("\n=== Message ===")
            print(format_verbose_output(message))
    else:
        answer, references = format_standard_output(result[-1])
        print(answer)
        if references:
            print("\nReferences:")
            for ref in references:
                print(ref)

    if save_output:
        save_output_to_file(result[-1].tool_calls[0]["args"], save_output)


@click.command()
@click.argument("question", required=True)
@click.option("--max-iterations", "-m",
              default=None,
              type=int,
              help="Maximum number of search-revise iterations")
@click.option("--model", "-l",
              default=None,
              help="OpenAI model to use (default: gpt-4-turbo-preview)")
@click.option("--max-results", "-r",
              default=None,
              type=int,
              help="Maximum number of search results to return per query")
@click.option("--word-limit", "-w",  # [TODO:] Remove this as it is not used
              default=250,
              type=int,
              help="Word limit for answers (default: 250)")
@click.option("--verbose", "-v",
              is_flag=True,
              help="Show detailed output including reflections and search queries")
@click.option("--save-output", "-s",
              type=click.Path(),
              help="Save the full response to a file")
def main(question: str,
         max_iterations: Optional[int],
         model: Optional[str],
         max_results: Optional[int],
         word_limit: int,
         verbose: bool,
         save_output: Optional[str]) -> None:
    """TETSUO research-focused question-answering system.

    Processes questions and returns detailed answers with citations based on current research.

    Environment:
        OPENAI_API_KEY: Valid OpenAI API key
        TAVILY_API_KEY: Valid Tavily API key

    Arguments:
        QUESTION: The research question to process

    Examples:
        Basic usage:
            dox-agent "What is quantum computing?"

        Verbose output with custom model:
            dox-agent -v -l gpt-4 "Explain dark matter"

        Save output to file:
            dox-agent -s output.json "History of AI"
    """
    load_dotenv()

    # Validate environment and update settings
    validate_environment()
    update_settings(max_iterations, model, max_results)

    # Create and invoke graph
    graph = create_graph()
    result = graph.invoke(question)

    # Process and display output
    process_and_display_output(result, verbose, save_output)


if __name__ == "__main__":
    main()
