# Channel Assignment — ASN-0040 review-69

**Date:** 2026-05-28 23:56

## Issue 1: Citation cycle between Bop and B1 (with an unnecessary dependency)
Reason: Purely internal — the fix rewrites Bop's freshness using only `next > max(children) ∈ S(p,d)` (S0, TA5(a), next definition) and drops the "by Bop" citation from B1. Both the corrected dependency chain and the antecedents it relies on are already present in the ASN.

## Issue 2: Proofs depend on results established later in the document
Reason: Internal presentation reorder. The logical dependency graph is already acyclic per the ASN's own contracts; the fix only resequences sections so antecedents precede consumers, requiring no design intent or implementation evidence.

## Issue 3: B0b restates B0a
Reason: Internal editorial decision between folding the dichotomy into B0a or reducing B0b to a one-line restatement. The relationship between B0a and B0b is fully determined by the ASN's own definitions.

## Issue 4: Over-elaboration in B6 necessity
Reason: Internal — the `t₁ ≠ 0` violation already discharges the singleton case, so dropping the redundant parenthetical is a self-contained edit derivable from the proof's own structure.
