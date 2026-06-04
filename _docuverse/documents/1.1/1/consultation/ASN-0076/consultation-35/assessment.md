# Channel Assignment — ASN-0076 review-35

**Date:** 2026-06-03 22:31

## Issue 1: The structural-vs-semantic caveat is restated in five places
Reason: Purely editorial deduplication — the distinction is already stated at the `τ_sup` definition and rigorously in E7; removing restatements requires no design intent or implementation evidence, only the ASN's own text.

## Issue 2: §The Composite previews E0's ValidComposite★ discharge
Reason: The preview paragraph is fully duplicated by E0's own discharge subsection; deleting it is internal to the ASN and needs no external channel.

## Issue 3: Redundant `#τ_sup ≥ 1` conjunct with inconsistent justification
Reason: The ASN already cites T0 (CarrierSetDefinition) guaranteeing `#t ≥ 1` for every `t ∈ T`; the redundancy and uniform rejustification are derivable from definitions already present.

## Issue 4: Redundant defensive justifications
Reason: Both removals (E2's parenthetical re-proof, E0's "First" precondition-level defense) concern prose already carried by L11a and K.λ+L4 within the ASN; the fix is internal editorial pruning.
