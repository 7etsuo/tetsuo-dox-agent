# Tetsuo Dox Agent

<div align="center">

![Tetsuo AI Logo](https://github.com/user-attachments/assets/8db7cb9d-0514-4f12-80ab-2027dc58d522)

[![Discord](https://img.shields.io/badge/Discord-Join%20Us-7289da?logo=discord&logoColor=white)](https://discord.gg/tetsuo-ai)
[![Website](https://img.shields.io/badge/Website-tetsuo.ai-blue?logo=internet-explorer&logoColor=white)](https://www.tetsuo.ai)

**$TETSUO Token on Solana**  
`Contract Address: 8i51XNNpGaKaj4G4nDdmQh95v4FKAxw8mhtaRoKd9tE8`

</div>

## Overview

Tetsuo Dox Agent is a research agent, designed for technically-focused responses with citations. Built on a graph-based architecture.

![image](https://github.com/user-attachments/assets/1ab31816-e66e-4df3-bd9e-d2f80e7b60ad)

The agent:

- Drafts detailed, technically accurate answers
- Performs systematic self-reflection and validation
- Conducts thorough research across multiple sources
- Iteratively refines responses based on discovered information
- Maintains strict citation standards for factual claims


## Key Features

- **Technical Focus**: Delivers purely factual, technical information without ethical commentary
- **Iterative Refinement**: Automatically improves answers through multiple rounds of:
  - Self-reflection and critique
  - Web-based research
  - Content revision
  - Citation verification
- **Research Integration**: Leverages Tavily Search API for real-time fact-checking and research
- **Structured Output**:
  - Primary response (250-word default limit)
  - Numbered citations [1], [2], etc.
  - Complete reference list with URLs and publication dates
  - Research queries and self-reflections (in verbose mode)
- **Quality Controls**:
  - Automatic fact verification
  - Citation management
  - Self-critique for information gaps
  - Technical accuracy verification

## Prerequisites

- Python 3.13
- Poetry for dependency management
- OpenAI API key (GPT-4 access required)
- Tavily API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/7etsuo/tetsuo-dox-agent.git
cd dox-agent
```

2. Install dependencies with Poetry:
```bash
# Initialize Poetry environment with Python 3.13
poetry env use python3.13

# Install dependencies
poetry install
```

3. Set up environment variables by creating a `.env` file:
```env
# Required Configuration
OPENAI_API_KEY=your_openai_key_here      # Required: OpenAI API key with GPT-4 access
TAVILY_API_KEY=your_tavily_key_here      # Required: Tavily API key for research

# Optional Configuration
MAX_ITERATIONS=3                         # Optional: Number of research-revise cycles (default: 3)
MODEL_NAME=gpt-4-turbo-preview           # Optional: OpenAI model choice
MAX_RESULTS=5                            # Optional: Maximum search results per query

# Optional LangSmith Integration
LANGCHAIN_API_KEY=your_langsmith_key     # Optional: For LangSmith tracing
LANGCHAIN_TRACING_V2=true                # Optional: Enable LangSmith tracing
LANGCHAIN_PROJECT=your_project_name      # Optional: LangSmith project name
```

### Docker installation
1. Build the Docker image:

```bash
docker-compose build
``` 

2. Set up environment variables in `.env` file (same as standard installation)

3. Run the agent using Docker:
```bash
docker-compose run --rm dox-agent "Your question here"
```


## Usage

![image](https://github.com/user-attachments/assets/06081610-d142-4a24-85e8-2679767618a9)

### Basic Command

Basic usage with default settings:
```bash
poetry run dox-agent "Your technical question here"
```

### Advanced Options

Customize the agent's behavior:
```bash
# Enable verbose output (includes reflections and research queries)
poetry run dox-agent --verbose "Your question"

# Customize iterations and model
poetry run dox-agent --max-iterations 4 --model gpt-4 "Your question"

# Save full response to JSON file
poetry run dox-agent --save-output results.json "Your question"
```

### Command Line Options

- `-m, --max-iterations`: Maximum research-revise cycles
- `-l, --model`: OpenAI model selection (default: gpt-4-turbo-preview)
- `-r, --max-results`: Maximum search results per query
- `-w, --word-limit`: Word limit for answers (default: 250)
- `-v, --verbose`: Enable detailed output including reflections
- `-s, --save-output`: Save complete response to JSON file
- `--help`: Display help message

### Output Format

Standard output includes:
- Technical response (within word limit)
- Numbered citations [1]
- Reference list with:
  - Author (when available)
  - Title
  - Publication/Website
  - URL
  - Publication Date

Verbose output (-v) adds:
- Self-reflection on response quality
- Identified knowledge gaps
- Research queries
- Search results summary

## Project Structure

```
dox_agent/
├── __init__.py
├── __main__.py
├── chains.py          # Chain definitions
├── cli.py             # Command line interface
├── config/            # Configuration and settings
│   ├── __init__.py
│   ├── constants.py
│   └── settings.py
├── exceptions.py      # Custom exceptions
├── graph/             # Graph-based architecture
│   ├── __init__.py
│   ├── builder.py
│   └── nodes.py
├── models/            # Pydantic models
│   ├── __init__.py
│   ├── answer.py
│   └── reflection.py
├── prompts.py         # Prompt templates
├── tools/             # Search tools
│   ├── __init__.py
│   └── search.py
└── types.py           # Type definitions
```

## Architecture Overview

The system operates through a graph-based architecture with three primary stages:

1. **Initial Draft**
   - Analyzes the question
   - Generates initial technical response
   - Performs self-critique

2. **Research Phase**
   - Generates targeted search queries
   - Executes web searches
   - Collects and processes results

3. **Revision Phase**
   - Incorporates new information
   - Updates citations
   - Refines technical accuracy
   - Maintains word limit

This process iterates according to the max_iterations setting or until optimal quality is achieved.

## Development

### Setting Up Development Environment

1. Clone and install as described above
2. Install development dependencies:
```bash
poetry install --with dev
```

### Adding New Features

1. **New Models**
   - Add Pydantic models in `models/`
   - Update type hints accordingly

2. **New Tools**
   - Implement tool classes in `tools/`
   - Register in tools registry if applicable

3. **New Graph Nodes**
   - Add nodes in `graph/nodes.py`
   - Update graph builder in `graph/builder.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Include docstrings for public interfaces
- Keep functions focused and modular

### Testing

```bash
# Run test suite (TODO: Add comprehensive tests)
poetry run pytest

# Run with coverage
poetry run pytest --cov=dox_agent
```

## Contributing

1. Fork the repository
2. Create your feature branch:
```bash
git checkout -b feature/your-feature-name
```
3. Commit your changes:
```bash
git commit -m 'Add some feature'
```
4. Push to the branch:
```bash
git push origin feature/your-feature-name
```
5. Open a Pull Request

### Pull Request Guidelines

- Include test cases for new features
- Update documentation as needed
- Follow existing code style
- One feature/fix per PR

## Acknowledgments

- Built with [LangChain](https://github.com/langchain-ai/langchain)
- Uses [LangGraph](https://github.com/langchain-ai/langgraph) for workflow management
- Search powered by [Tavily](https://tavily.com/)
- Developed with [OpenAI](https://openai.com/) GPT-4 technology

## Support

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
