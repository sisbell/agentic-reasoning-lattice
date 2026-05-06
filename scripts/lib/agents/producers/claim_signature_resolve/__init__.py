"""Claim signature-resolve agent — producer for per-claim signature sidecars.

Public surface:
- ClaimSignatureResolveAgent — Agent class fired by the
  claim-signature-resolve trigger. One fire = one claim's signature
  sidecar resolution (write or version advance).
- extract_signature_changes — LLM-call helper used by the agent.
"""

from .agent import ClaimSignatureResolveAgent
from .helpers import SignatureChanges, extract_signature_changes

__all__ = [
    "ClaimSignatureResolveAgent",
    "SignatureChanges",
    "extract_signature_changes",
]
