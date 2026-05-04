"""Note-review agent — Dijkstra-style proof-review of an ASN.

LLM invocation that reads an ASN's prose, vocabulary, foundation
statements, and open issues; produces a structured review with REVISE
/ OUT_OF_SCOPE findings and a VERDICT line.

Pure agent: returns the review text + verdict + elapsed time. No
substrate writes, no filesystem mutations beyond reading. The
orchestrator (`lib/orchestrators/note_converge.py`) commits the
review document, emits substrate links, and handles the resolved-
issues sweep.
"""

from .agent import extract_note_findings, run_note_review

__all__ = ["extract_note_findings", "run_note_review"]
