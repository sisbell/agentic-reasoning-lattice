"""Citation-resolve agent — Sonnet depends/forward classifier.

LLM invocation that reads a claim's prose plus the existing
classifications and produces structured (classifications, retractions)
edit lists. No substrate side effects, no filesystem writes — those
happen in the orchestrator (`lib/orchestrators/citation_resolve.py`).
"""

from .body import CitationClassifications, extract_citation_classifications

__all__ = ["CitationClassifications", "extract_citation_classifications"]
