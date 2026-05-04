"""Signature-resolve agent — Sonnet introduces/removes extractor.

LLM invocation that reads claim prose + upstream signatures + existing
signature + notation primitives, and produces a structured
(introduces, removes) edit list for the claim's signature sidecar.

Pure agent body: prompt rendering, LLM call, response parsing. No
substrate side effects, no filesystem writes — those happen in the
orchestrator (`lib/orchestrators/signature_resolve.py`).
"""

from .body import SignatureChanges, extract_signature_changes

__all__ = ["SignatureChanges", "extract_signature_changes"]
