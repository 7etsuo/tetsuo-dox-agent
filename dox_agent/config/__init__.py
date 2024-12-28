"""
Configuration package for dox-agent.

This package manages all configuration aspects of the system including:
    - Environment variables
    - API keys and credentials
    - System constants
    - Runtime settings

Components:
    - settings: Central configuration object with environment variables and app settings
    - constants: System-wide constant values

Usage:
    from dox_agent.config.settings import settings
    from dox_agent.config.constants import WORD_LIMIT
"""

from .settings import settings
from .constants import WORD_LIMIT

__all__ = ["settings", "WORD_LIMIT"]
