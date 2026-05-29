# Review of ASN-0036

## REVISE

### Issue 1: Forward-reference accretion in the S5 proof
**ASN-0036, S5 proof, opening paragraph**: "The claim is a non-entailment: it asks only for a model of S0–S3 with unbounded multiplicity, so we verify S0–S3 and nothing more. (That these witnesses also happen to satisfy the always-on invariants introduced later — S7*, S8-*, D-* — is immaterial to the claim and is not part of the argument.)"
**Problem**: This is meta-prose, not reasoning. The parenthetical enumerates downstream consumers (`S7*, S8-*, D-*`) and defends a scope decision rather than advancing the proof — exactly the forward-reference accretion this note's `review-mode.anti-bloat` classifier targets. It reads as relocated reviser justification (the prior cycle's "S5 scope/order defect"), now sitting in the proof body. A reader must skip past it to reach the actual construction.
**Required**: Delete the parenthetical and the "so we verify S0–S3 and nothing more" defense. The proof already verifies S0–S3 per construction; stating *what* is verified is enough without justifying *why nothing else* is.

### Issue 2: Defensive precondition gloss in D-CTG-depth
**ASN-0036, D-CTG-depth, Preconditions**: "`m ≥ 3` (the lemma's non-triviality bound, additional to S8-depth — at `m = 2` the conclusion holds vacuously since the range of shared components 2 through `m − 1` is empty)."
**Problem**: The parenthetical explains why the bound is needed rather than stating the precondition. The vacuous-at-`m=2` observation is already made operationally in D-SEQ Step 1 (Case m = 2), so this duplicates reasoning across sections.
**Required**: State the precondition as `m ≥ 3` and let D-SEQ's Case-`m=2` handle the boundary, or move the boundary remark to a single canonical site.

### Issue 3: Redundant scoping prose at the insertion-position section head
**ASN-0036, "Valid insertion position" intro**: "We work with the arrangement M(d) and the contiguity constraint D-CTG from above, restricted to the text subspace `S = 1`, using `V_1(d)` as fixed at the abbreviation paragraph above."
**Problem**: Pure navigation prose ("from above," "as fixed at the abbreviation paragraph above") that advances no claim. The definitions that follow already cite their dependencies (D-MIN, D-CTG, D-SEQ) in their Formal Contracts.
**Required**: Drop the sentence; the predicate definitions carry their own preconditions.

## OUT_OF_SCOPE

### Topic 1: Operation-layer preservation of D-CTG/D-MIN/S2
The note repeatedly gestures at how INSERT/DELETE/COPY maintain contiguity (and the Open Questions list this explicitly). Per the Scope section, operation-specific frame conditions belong in a future ASN, not here.

---

Substantively the mathematics holds. The S8 partition (coverage + within-subspace incompatibility lemma + cross-subspace via T5/T10), the D-CTG-depth infinite-intermediate contradiction against S8-fin, and the D-SEQ four-step assembly are each complete, with boundary cases (`dom(M(d)) = ∅`, `m = 2`, `j = m`) covered and a concrete worked example exercising S0/S3/S7/S8/D-SEQ across four states. The findings are accumulated meta-prose around forward references, not proof gaps.

VERDICT: REVISE
