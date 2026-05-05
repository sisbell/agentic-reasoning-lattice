"""Claim-describe agent — generates / refreshes a claim's description sidecar.

Public:
- ClaimDescribeAgent — Agent class fired by the claim-describe trigger.
"""

from __future__ import annotations

from .agent import DESCRIBE_MODEL, ClaimDescribeAgent


__all__ = [
    "DESCRIBE_MODEL",
    "ClaimDescribeAgent",
]
