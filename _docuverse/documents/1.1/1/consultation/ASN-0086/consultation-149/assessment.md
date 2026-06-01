# Channel Assignment — ASN-0086 review-149

**Date:** 2026-06-01 03:54

## Issue 1: Clause (c) of substrate-conforming presupposes the contiguity L-ContiguousPrefix proves
Reason: The fix is editorial restatement of clause (c) using machinery already in the ASN (`a_emit`'s `inc(ℓ_prev, 0)` / first-emission rule, or an explicit "read jointly with L-ContiguousPrefix" note). No design intent or implementation evidence is needed.

## Issue 2: Triple deferral to NestedLinkWitness across three sections
Reason: Pure consolidation — state the `inc(a, 1)` witness once in the Remark and have the two definitions cite it by name. Derivable from the ASN's own structure.

## Issue 3: Document-ordering / scope-justification meta-prose
Reason: Both edits are deletions of meta-prose (root-state rationale, proof-roadmap sentence); the surrounding content stands unchanged. Internal.
