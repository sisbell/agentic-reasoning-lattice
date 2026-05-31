# Channel Assignment — ASN-0093 review-26

**Date:** 2026-05-31 05:34

## Issue 1: Dangling `(a), (b), (c)` reference in the Link-withdrawal Open Question
Reason: Purely internal editorial fix — the three formulations (value transition, arrangement-side, embedded-marker) are already named in the preceding prose; the fix is to label them or rewrite the sentence inline. No design intent or implementation evidence needed.

## Issue 2: Duplicate deferrals across Scope and Open Questions
Reason: Internal structural cleanup — the Scope "Deferred" bullets and Open Questions restate the same deferrals; consolidating to one statement per topic is derivable from the note's own content.

## Issue 3: Document-address discipline stated three times
Reason: Internal deduplication — the same point (K.σ structural-only, baptism is higher-layer) appears three times; collapsing to the K.σ section requires no external input.

## Issue 4: ChainDiscipline lemma duplicates the preceding paragraph
Reason: Internal editorial merge — the paragraph and the lemma state the same `A_·(d) = S(b_·(d), 1)` identity; folding one into the other is derivable from the note alone.

## Issue 5: Defensive / scope meta-prose around forward references
Reason: Internal deletion — the flagged sentences ("load-bearing," "not weakened," "imported only at stream level") are justification noise already licensed by the B6-validity discharge; removing them needs no external channel.

## Issue 6: Essay content in discharge-matrix cells
Reason: Internal relocation — moving the L0/L14 derivations out of matrix cells into a short lemma or precondition prose is a formatting fix derivable from the note's existing arguments.

## Issue 7: Redundant structural preconditions on K.α / K.λ
Reason: Internal — the note already argues the structural clauses (`zeros=3`, `E(·)₁=s_C`, `#E≥2`, `origin=d`) follow from the chain-emission clause via ChainUniformZeroCount/DisjointSubAllocatorChains/ChainUniformLength; deciding whether to demote them to derived postconditions is an authoring choice resolvable from the ASN's own proofs.
