"""
Model definitions for the question-answering process.

Dependencies:
    - pydantic: For BaseModel and Field
    - dox_agent.models.reflection: Reflection model for capturing revision logic

Classes:
    - AnswerQuestion: Represents the structure of an answer with reflection and queries
    - ReviseAnswer: Extends AnswerQuestion to include references
"""

from typing import List
from pydantic import BaseModel, Field
from .reflection import Reflection


class AnswerQuestion(BaseModel):
    """Answer the question."""
    answer: str = Field(
        description="~250 word detailed answer to the question.")
    reflection: Reflection = Field(
        description="Your reflection on the initial answer.")
    search_queries: List[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )


class ReviseAnswer(AnswerQuestion):
    """Revise your original answer to your question."""
    references: List[str] = Field(
        description="Citations motivating your updated answer."
    )
