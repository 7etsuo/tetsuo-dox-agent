"""
Model for capturing critiques of the current answer.

Fields:
    - missing: Description of missing elements
    - superfluous: Description of superfluous or unnecessary parts
"""

from pydantic import BaseModel, Field


class Reflection(BaseModel):
    missing: str = Field(
        description="Analysis of key information, perspectives, or evidence that would strengthen the answer. "
        "This includes potential gaps in reasoning, missing contextual details, unexplored aspects, "
        "or relevant counterarguments that should be addressed."
    )
    superfluous: str = Field(
        description="Identification of content that could be removed or condensed for clarity and focus. "
        "This includes redundant information, tangential details, or overly verbose explanations "
        "that don't meaningfully contribute to answering the question."
    )
