"""Claim-finding-override agent — second-opinion classifier on REVISE/OBSERVE.

The reviewer self-classifies each finding (REVISE or OBSERVE). This
agent runs an independent Sonnet pass against the strict test ("would
the artifact be wrong without the fix?") and overrides the reviewer's
class when the two disagree. The original reviewer call is preserved
in the body as audit history.

Claim-layer only. The note layer's REVISE/OUT_OF_SCOPE classification
is encoded in section headers and parsed without an override pass.
"""

from .agent import apply_classifier_verdict, classify_finding

__all__ = ["apply_classifier_verdict", "classify_finding"]
