# Revision Categorization — ASN-0043 review-3

**Date:** 2026-03-16 22:11

## Issue 1: Structural attribution gap — missing S7a analog for link addresses
Category: INTERNAL
Reason: The ASN already contains the implementation evidence (allocation via `findisatoinsertmolecule` producing element-level tumblers under the document prefix) and the `origin`/`home` definitions. The fix is to state property L1a explicitly or present ownership as a definitional commitment — a formalization gap, not an evidence gap.

## Issue 2: L11 formal statement — "distinct links" is undefined
Category: INTERNAL
Reason: The prose already explains the correct meaning (entity-distinctness, not value-distinctness), and S4 from ASN-0036 provides the exact pattern to follow. The fix is restating the formal expression to match.

## Issue 3: L9 formal statement — permission stated as negated invariant
Category: INTERNAL
Reason: The intended semantics (ghost types are permitted, not required) are clear from prose and Nelson quotes already in the ASN. The fix is reformulating the quantifier structure following S5's existential/witness pattern — a logical notation fix.

## Issue 4: No concrete example
Category: INTERNAL
Reason: All definitions, span arithmetic rules (T12, TA5), and subspace conventions needed to construct a worked example are already present across ASN-0034, ASN-0036, and this ASN. The task is building a concrete instance from existing material and verifying each property against it.
