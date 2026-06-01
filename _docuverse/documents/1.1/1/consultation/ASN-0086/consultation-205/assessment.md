# Channel Assignment — ASN-0086 review-205

**Date:** 2026-06-01 15:43

## Issue 1: "Working domain" paragraph announces downstream derivations
Reason: Pure prose-deletion of a forward-reference inventory; the lemmas L-ContiguousPrefix and R0a are stated and proved in their own sections, so removing the announcement requires no design intent or implementation evidence.

## Issue 2: Nullify precondition P0f is redundant under PC
Reason: The entailment `PC ∧ P0 ⟹ P0f` is established within the note itself (P0f "holds automatically … under L-ContiguousPrefix"), so dropping or compressing the clause is internally derivable.

## Issue 3: "Corollary (reduction to Emit_K)" is a restatement of its own definition
Reason: The corollary restates the immediately preceding Definition by construction; folding the one substantive sentence in and removing the proof framing is a structural edit needing nothing external.

## Issue 4: Duplicate prose in the wp domain discussion
Reason: Two consecutive paragraphs state the same layer-commitment/address-vs-shape proposition; merging them is internal prose deduplication requiring no channel input.
