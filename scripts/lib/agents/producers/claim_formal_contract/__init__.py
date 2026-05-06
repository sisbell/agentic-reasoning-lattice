"""Claim formal-contract producer package.

Synthesizes the Formal Contract section in a claim's md body. Lifted
from the previous imperative produce_contract phase.
"""

from .agent import ClaimFormalContractAgent

__all__ = ["ClaimFormalContractAgent"]
