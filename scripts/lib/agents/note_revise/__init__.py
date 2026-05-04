"""Note-revise agent — apply per-finding fixes to an ASN.

LLM invocation that reads the ASN, the discovery methodology prompt,
and a list of open revise findings; instructs Claude (with Edit
tools) to fix each finding in the note and close the corresponding
comment via convergence-link-resolution.py.

Pure agent: returns the Claude SDK invocation result + elapsed time.
No substrate-writing logic in the agent itself — Claude does the
writes via its tools, and the substrate-mediated comment closure
happens through convergence-link-resolution.py invoked by the agent.
"""

from .agent import build_prompt, run_revise_pass

__all__ = ["build_prompt", "run_revise_pass"]
