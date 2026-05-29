# Review of ASN-0040

This ASN is formally mature — the core proofs (B7 namespace disjointness, B1 contiguous prefix, B8 co-reachable uniqueness, B9 unbounded extent) are case-complete, handle the length split and nesting/non-nesting parent boundaries, and the worked trace exercises d=1, d=2, and both B7 disjointness witnesses. The freshness argument in Bop correctly avoids leaning on contiguity. My findings are confined to residual meta-prose of the kind this note's anti-bloat classifier targets.

## REVISE

### Issue 1: Methodological justification in the S(p,d) section
**ASN-0040, S(p,d) / "sibling stream"**: "The sibling stream S(p, d) corresponds to the domain of a foundation allocator (T10a, ASN-0034) — base c₁ = inc(p, d) followed by repeated inc(·, 0) — though we prove the stream properties we need below directly from the increment algebra."
**Problem**: This advances no reasoning. It explains *why the proof method is what it is* (direct from increment algebra rather than via T10a) — exactly the allocator cross-reference the prior cycle was trimming (commit `trim allocator cross-references`). The stream properties S0/S1 stand on their own proofs; the T10a analogy is commentary the precise reader must skip.
**Required**: Delete the sentence. If a foundation pointer is wanted, it adds nothing the S0/S1 proofs don't already establish.

### Issue 2: Defensive "what is not required" prose around B₀ conf.
**ASN-0040, B_fin section**: "The invariant proofs that follow induct over transition sequences from the initial state. They require a conforming seed and a finiteness guarantee that each transition preserves." and B₀ conf.: "Non-emptiness is not among them; this ASN neither requires nor establishes it."
**Problem**: The first is roadmap prose previewing proof structure the proofs themselves carry. The second is a defensive justification stating what the seed condition does *not* include — the flagged "imagines/excludes a case" defensive pattern. Neither advances B₀ conf. or B_fin.
**Required**: Drop the B_fin preamble sentence and the "Non-emptiness…" clause. State B₀ conf.'s three conditions and move on.

### Issue 3: Comparative essay distinguishing B1 from foundation T9
**ASN-0040, after B10**: "The gap between T9 (ForwardAllocation) and B1 is the *no-skip property*… T9 says addresses increase; B1 says they increase *contiguously*. The difference is the guarantee that every ordinal from 1 through m is represented, which T9 alone does not assert."
**Problem**: B1's statement ("children = {c₁,…,cₘ}") and proof already establish contiguity outright. This paragraph re-characterizes B1's significance by contrast with a foundation property — a "what this note adds relative to the foundation" essay sitting in a structural slot, not a step in any argument.
**Required**: Remove, or compress to at most the single clause that B1 is strictly stronger than monotonicity, inside B1's own statement.

## OUT_OF_SCOPE

### Topic 1: B3 Ghost Validity touches content storage
**Why out of scope**: Content storage is listed out of scope, and B3 constrains a future `Occupied` predicate. This is acceptable as a *forward requirement* — it defines no content operation and ghost elements are intrinsic to baptism (Nelson). Noted only to confirm it was considered; no change needed unless the project prefers to relocate the forward requirement to the content-storage ASN.

VERDICT: REVISE
