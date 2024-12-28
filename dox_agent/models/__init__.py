"""
Data models package for dox-agent.

This package contains Pydantic models that define the structure of data
used throughout the question-answering system. These models provide validation,
serialization, and clear interfaces for the system's data structures.

Models:
    - AnswerQuestion: Base model for initial answers with reflection
    - ReviseAnswer: Extended model for revised answers with references
    - Reflection: Model for capturing answer critiques and improvements

Usage:
    from dox_agent.models.answer import AnswerQuestion, ReviseAnswer
    from dox_agent.models.reflection import Reflection
"""

from .answer import AnswerQuestion, ReviseAnswer
from .reflection import Reflection

__all__ = ["AnswerQuestion", "ReviseAnswer", "Reflection"]
