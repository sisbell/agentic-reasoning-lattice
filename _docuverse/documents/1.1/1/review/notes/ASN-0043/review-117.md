# Review of ASN-0043

This is a careful, near-complete note: the worked example exercises the hard cases (multi-span L5, coverage-vs-decomposition L8, discrimination), the FSP/FSE factoring is sound, and I found no correctness gap in the chain constructions (L1c, FSE, L9 Case A/B), the coverage arithmetic (Step 6), or the L0a/T7 disjointness discharge. The remaining issues are the meta-prose accretion the `review-mode.anti-bloat` classifier flags.

## REVISE

### Issue 1: L7's "Structurally." gloss restates the L7 claim in different words
**ASN-0043, L7 — DirectionalFlexibility**: the statement reads "The invariants L0–L14 and L-fin impose no constraint on which of the from/to slots carries directional significance; any directional interpretation is determined by the link type, outside the link structure." The following paragraph reads "*Structurally.* The invariants of L0–L14 and L-fin quantify only over addresses, endset membership, and slot position; not one of them predicates on which slot is source and which is target."
**Problem**: The "Structurally." paragraph says the same thing as the claim it sits under — "no constraint on which slot is source/target" reworded as "not one of them predicates on which slot is source and which is target." This is the "two paragraphs say the same thing in different words" pattern; it forces the reader past a restatement to reach the Nelson quote that actually adds content.
**Required**: Delete the "Structurally." gloss; the L7 statement plus the Nelson quotation already carry the claim.

### Issue 2: FSP's closing L11a paragraph addresses a property outside the lemma's stated conclusion
**ASN-0043, FSP — FreshSiblingConformance, final paragraph**: "L11a is not a state-local invariant but a cross-event lemma (LinkUniqueness); it holds in `Σ'` automatically, since FSP preserves L1c and S7d, from which GlobalUniqueness (ASN-0034) re-derives address distinctness across the distinct allocation events of `dom(Σ'.L)`."
**Problem**: FSP's stated conclusion is the state-local L-/S-invariants plus L12/L12a. L11a is excluded by that scope by design (it is proven in its own section from L1c + S7d + GlobalUniqueness). The paragraph is defensive prose anticipating a "but what about L11a?" objection — the "paragraph imagines a case the claim's carrier already excludes" pattern. It re-derives, in miniature, the argument L11a already carries.
**Required**: Remove the paragraph. If a pointer is wanted, a half-sentence in L11b/L11a noting that fresh-sibling extensions preserve L11a's premises suffices, placed where L11a lives.

### Issue 3: L9 "Selection of d'" justifies the construction rather than performing it
**ASN-0043, L9 witness, *Selection of `d'`***: "L1a requires `home(a) ∈ dom(Σ'.M)`, and S7d requires every entry of `dom(Σ'.M)` to be a node in the system's allocator tree 𝒯 produced by a T10a allocation event. By the L9 precondition `dom(Σ.M) ≠ ∅`, pick any `d ∈ dom(Σ.M)` and set `d' = d`. ... Reusing the existing arrangement keeps `Σ'.M = Σ.M`, so no new document allocation event is introduced."
**Problem**: The first sentence explains *why* `d'` must be a valid allocated document before constructing it, and the last clause defends *why* a complication (a fresh document allocation) is avoided. Both are motivation/defensive framing around a one-line construction ("pick any `d ∈ dom(Σ.M)`; `d` is T4-valid by DocVal"). This is the "prose explains why X is needed rather than what it does" pattern.
**Required**: Reduce to the construction: pick `d ∈ dom(Σ.M)` (nonempty by precondition), set `d' = d`, T4-valid with `zeros(d') = 2` by DocVal, `d' ∈ dom(Σ'.M)` since `Σ'.M = Σ.M`.

## OUT_OF_SCOPE

### Topic 1: Global content-subspace constant
The note's first Open Question (extending content-side disjointness from the `s_C`-slice to all of `dom(Σ.C)`) is a genuine future-ASN item, already correctly parked in Open Questions and scoped out of L0a/L14/L14a. No action needed.

VERDICT: REVISE
