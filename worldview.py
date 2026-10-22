"""The worldview now lives as structured, local philosophical principles.

This module remains a convenient entry point for inspecting and editing the
knowledge base. There is no system prompt, language model or API integration.
The original prose is preserved in Git history.
"""

from philosophy.knowledge import PRINCIPLES, PRINCIPLES_BY_ID, Principle
from philosophy.lexicon import RELATIONSHIPS
from philosophy.universal import LENSES
from philosophy.concepts import CHAINS, MODELS, SYNTHESES

__all__ = ["Principle", "PRINCIPLES", "PRINCIPLES_BY_ID", "RELATIONSHIPS", "LENSES", "CHAINS", "MODELS", "SYNTHESES"]
