"""Claim-revise agent — apply per-finding fixes to a claim's .md.

LLM invocation that reads a finding (title + body) and edits the
claim file via Claude's Edit tool. Closes the corresponding comment
via `convergence-link-resolution.py`. Same agent invoked from both
whole-ASN reviews and regional cone reviews — the call site supplies
the comment_id so the agent can close it.
"""

from .agent import revise

__all__ = ["revise"]
