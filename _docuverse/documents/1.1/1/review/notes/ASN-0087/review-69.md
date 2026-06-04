# Review of ASN-0087

## REVISE

### Issue 1: Editorial relabeling in the worked example's reflexive variant
**ASN-0087, A Worked Example (reflexive variant)**: "This variant is precisely the boundary M-FreshExcl / M-Reflexive isolate — the reflexive route is reachable only by violating standard authoring, which is why the standardly-authored discipline structurally excludes it."
**Problem**: The computation immediately above already establishes both facts it summarizes: `coverage(e₁') ∋ ℓ` fires the reflexive disjunct, and `e₁'` violates standard authoring (`coverage(e₁') ∩ F ⊄ dom(Σ.C) ∪ dom(Σ.L)`). The closing sentence restates M-Reflexive's own clause ("Under StandardAuthoring the reflexive case is structurally excluded") without adding reasoning — meta-prose the reader must skip past.
**Required**: Delete the sentence; the concrete computation carries the content.

### Issue 2: Interpretive restatement in Permanence of the Recording
**ASN-0087, Permanence of the Recording**: "The implication is that once recorded, the endsets' addressing intent is permanent: each coverage `coverage(Σ'.L(ℓ).eᵢ)` is fixed across every reachable state, so the link names the same set of I-addresses for all time."
**Problem**: This re-says the formal coverage-equality derived one sentence earlier (`coverage(Σ''.L(ℓ).eᵢ) = coverage(Σ'.L(ℓ).eᵢ)`) in essay register ("addressing intent," "for all time"). Two sentences saying the same thing in different words.
**Required**: Drop the paragraph, or fold its one operative phrase into the formal statement.

## OUT_OF_SCOPE

None — the Open Questions appropriately defer ghost-type endsets, forward-reaching coverage, and deferred-consistency to future ASNs.

Substantively the note is sound: the K.λ ; K.μ⁺_L decomposition and forced order are correct; the S2, D-CTG★, D-SEQ★, and D-MIN★ proofs handle the empty/non-empty link-subspace split with arbitrary-depth contiguity argued directly (not by "similarly"); the wp computation reaches a non-trivial reflexive case; the worked example verifies discoverability concretely; invariant coverage matches ASN-0047's three-class theorem; and all cross-references are to foundation ASNs.

VERDICT: REVISE
