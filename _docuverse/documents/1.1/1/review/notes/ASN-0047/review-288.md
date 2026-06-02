# Review of ASN-0047

## REVISE

### Issue 1: "Empty content source ⟹ ex nihilo, not fork" stated three times
**ASN-0047, K.δ (Elementary transitions), J4 (Coupling), and J4 Properties table**:
- K.δ: "When the source's content subspace is empty, fork reduces to K.δ alone."
- J4 table: "content-subspace-empty source is ex nihilo (K.δ), not fork"
- J4 prose: "so when d_op's content subspace is empty (V_{s_C}(d_op) = ∅) the fork definition does not apply, and creation from such a source is ex nihilo (K.δ alone), not a fork."

**Problem**: The same fact appears in three sections, the last two within a few paragraphs of each other. This is the `review-mode.anti-bloat` "two paragraphs say the same thing" pattern. The J4 prose additionally re-litigates why `V_{s_C}(d_op) ≠ ∅` rather than `M(d_op) ≠ ∅` is the precondition — a justification of a precondition choice that the precondition statement already settles.
**Required**: State the empty-source-is-ex-nihilo fact once (at the Fork definition, where the precondition `V_{s_C}(d_op) ≠ ∅` lives) and delete the two restatements.

### Issue 2: Duplicated "forced by a design choice, not the calculus" rationale across J1★ and J1'★
**ASN-0047, *Scoped coupling constraints* (J1★ and J1'★ derivations)**: The J1★ derivation closes "Therefore, to maintain P4★, K.ρ must co-occur... — which is J1★ above," and the J1'★ derivation closes with the parallel "we *impose* this as the composite-scoped coupling J1'★ below... The coupling is forced by a *design choice*, not by the calculus alone: Nelson commits to a permanent reverse index and Gregory confirms..."
**Problem**: Both derivations append the same "the wp calculus motivates but does not force; the design choice + Nelson/Gregory evidence forces it" meta-commentary. The point is identical in both directions; repeating the framing twice is essay content padding the structural derivation slots. The related self-referential signposting ("This is the load-bearing fact the discharge rests on..." in P4a; "What this step establishes is the matching realisability direction" in Step (B); "Necessity does not consume CL-UNIQ directly" in the necessity proof) describes the proof's own bookkeeping rather than advancing it.
**Required**: State the design-choice-vs-calculus observation once (it applies symmetrically to both couplings) and trim the proof-internal "what this step does / what it consumes" narration to the substantive inferences.

### Issue 3: S8★(s_L) non-canonicity asserted twice in succession
**ASN-0047, *Amendments to existing transitions*, S8★ definition (Link subspace route)**: "...the link-subspace partition is non-canonical. Non-canonicity is a property of S8★(s_L) itself: dropping (c) is exactly the assertion that S8★(s_L) fixes no canonical run-partition."
**Problem**: The second sentence restates the first ("non-canonical" → "fixes no canonical run-partition"; "dropping (c)" was already the stated cause). The paragraph reaches its conclusion and then re-states it in different words.
**Required**: Keep the first sentence; delete the "Non-canonicity is a property of S8★(s_L) itself..." restatement.

### Issue 4: Multi-position first content insertion under-specified by the cited predicate
**ASN-0047, K.μ⁺ precondition, *First content insertion***: "when V_{s_C}(d) = ∅, the depth of the first content V-position is pinned by `ValidFirstInsertionPosition(d, v, m)`... which for any chosen `m ≥ 2` fixes the unique well-formed first content V-position `v`."
**Problem**: `ValidFirstInsertionPosition` (ASN-0036) is a predicate over a **single** V-position, but K.μ⁺ is multi-position (`dom(M'(d)) ⊃ dom(M(d))` may add several mappings at once). For a first insertion of K > 1 content positions into an empty content subspace, the cited predicate constrains only the minimum `[s_C,1,…,1]`; the remaining K−1 positions are pinned not by this predicate but by the D-CTG★ / D-MIN★ / D-SEQ★ postconditions on the resulting `M'(d)`. The prose ties first-insertion well-formedness to the single-position predicate alone, leaving the multi-position case's position set implicit.
**Required**: One clause noting that the full first-insertion block `{[s_C,1,…,1,k] : 1 ≤ k ≤ K}` is fixed by the K.μ⁺ D-CTG★/D-MIN★ postconditions (equivalently D-SEQ★ at Σ'), with `ValidFirstInsertionPosition` fixing the minimum.

## OUT_OF_SCOPE

### Topic 1: Link provenance
R is typed `T_elem × E_doc` and P7 grounds entries in `dom(C)`, so links arranged via K.μ⁺_L receive no provenance record. This is consistent with the design and already named in the open questions ("additional permanence properties... for content that participates in link endsets"). Not an error here.

### Topic 2: Interior-position insertion with renumbering
K.μ⁺ appends content (shift of max) or seeds the first block; genuine interior insertion with V-position compaction is a named-operation (INSERT/DELETEVSPAN) concern, correctly deferred via the open question on renumbering-aware contraction.

VERDICT: REVISE
