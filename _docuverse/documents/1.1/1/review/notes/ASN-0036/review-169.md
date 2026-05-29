# Review of ASN-0036

The mathematical core of this note is sound. I checked the S8 partition proof (coverage, within-subspace incompatibility lemma, cross-subspace uniqueness via T5/T10), the D-CTG-depth infinite-intermediate construction, and the D-SEQ four-step assembly — the tiling claim, usually the most hand-waved, is proven rigorously here, with the empty-arrangement boundary handled explicitly. The findings below are accretion and misplacement, consistent with the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: Revision-history meta-prose in the Properties table
**ASN-0036, end of "Properties Introduced"**: "The label gaps `S6` (between S5 and S7a) and `S7c` (within the S7 family) are intentional: both were retired in revision, and no claim in this ASN depends on them."
**Problem**: This advances no reasoning about the strand model — it documents the note's own edit history. A reader following the invariant structure skips past it. This is exactly the "explains why ... rather than what it says" accretion the classifier targets.
**Required**: Remove. If gap-numbering must be acknowledged, a renumbering to S0–S6 contiguous would eliminate the need for the note entirely.

### Issue 2: S4 proof restates a decidability claim already made in prose, and proves a property outside its contract
**ASN-0036, S4 proof**: "Finally, the distinctness `a₁ ≠ a₂` is decidable from the addresses alone by T3 (CanonicalRepresentation, ASN-0034)... No value comparison is required."
**Problem**: S4's postcondition is `a₁ ≠ a₂` (regardless of value equality) — decidability is not a stated postcondition. The proof's closing paragraph proves something the contract does not claim, and it duplicates the body prose ("The structural test for shared identity is address equality, decidable from the addresses alone (T3)..."). Two paragraphs saying the same thing, one in the wrong slot.
**Required**: Either drop the decidability sentence from the proof (the proof closes correctly the moment GlobalUniqueness yields `a₁ ≠ a₂`), or add decidability as a postcondition and prove it once. Do not state it in both prose and proof.

### Issue 3: S7 "Permanence" paragraph invokes S4 for a case the setup already excludes
**ASN-0036, S7 proof, Permanence**: "By S4 (origin-based identity), distinct allocation events produce distinct addresses, so the address `a` itself is never reassigned or reused."
**Problem**: Permanence of `origin(a)` follows entirely from `a` being a fixed component sequence (so `a` does not change once it exists by S0) and `origin` being a deterministic function of those components. Reassignment of `a` is not a state transition the model admits — `dom(C)` only grows (S1) and addresses are tumblers, not mutable cells. The S4 sentence answers a worry the framework already forecloses; it pads the derivation rather than advancing it.
**Required**: Drop the S4 sentence from the Permanence step. The chain `a` immutable (fixed tumbler) + `origin` deterministic on components → `origin(a)` constant is complete and tighter.

## OUT_OF_SCOPE

### Topic 1: Operations preserving the contiguity invariants
The note proves D-CTG/D-MIN/D-SEQ hold of well-formed *states* and exhibits them across Σ₀–Σ₃ in the worked example, but never proves that INSERT/DELETE/COPY/REARRANGE *re-establish* them. This is correct to defer — operation frame/postconditions are explicitly out of scope and already named in Open Questions.

### Topic 2: Contiguity for non-text subspaces
D-CTG, D-MIN, D-SEQ are stated only for `V_1(d)` (text). Whether the link subspace (subspace 2) carries analogous contiguity is genuinely new territory tied to links/endsets, not a gap in this ASN.

### Topic 3: Constraints on the value domain `Val`
`Val` is deliberately opaque. Whether it must be uniform or support heterogeneous first-class content types is a future question (already listed under Open Questions).

VERDICT: REVISE
