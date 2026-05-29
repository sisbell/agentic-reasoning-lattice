# Review of ASN-0053

The algebra is, on the mathematics, sound: I checked S0–S11d, the WF lemma, the SC routing, and the S8/S9 construction-uniqueness pair, and the proofs hold (boundary discharges, exhaustiveness of the SC routing, and the loop invariant in S8 all close). My findings are about accreted meta-prose and one dangling forward reference — which this note's `review-mode.anti-bloat` classifier asks me to surface at source.

## REVISE

### Issue 1: WF introduced by its use-sites, not its meaning
**ASN-0053, WF (WellFormedSpanFromEndpoints)**: "We isolate the well-formedness verification that recurs at every span-construction site below, so that no later proof need re-derive it."
**Problem**: This introduces the lemma by enumerating downstream consumers ("recurs at every span-construction site below… so no later proof need re-derive it") rather than advancing what WF states. It is the "definition's introduction enumerates downstream consumers" pattern. WF's statement and proof already stand on their own.
**Required**: Delete the sentence. Let the lemma statement (s < r, #s = #r ⟹ (s, r ⊖ s) is well-formed with reach r) introduce itself.

### Issue 2: The a = b "degenerate case" is excluded and never handled
**ASN-0053, The reach function**: "When a = b, b ⊖ a produces the zero tumbler and a ⊕ (b ⊖ a) is not well-formed (TA0 requires w > 0), so this degenerate case is handled separately."
**Problem**: Every span endpoint pair satisfies start(σ) < reach(σ) by TA-strict, so a = b never arises for any span in this ASN. The clause imagines a case the carrier precondition excludes, and the promise "handled separately" is never delivered anywhere in the note — a dangling forward reference. This is reviser drift.
**Required**: Remove the sentence. Width recovery is only ever invoked for a < b (start < reach); the degenerate case has no referent here.

### Issue 3: Forward defer to S9 inside the S8 construction
**ASN-0053, S8 (NormalizationExistence), Construction**: "The construction below depends only on the non-decreasing order of starts, not on the tie-breaking choice — uniqueness of the emitted span-set is inherited from S9."
**Problem**: S8's job is existence; it should produce a normalized equivalent and prove J. The clause "uniqueness … is inherited from S9" defers to a downstream result to justify a construction detail that S8 does not need (tie-independence is not required for S8's claim — any normalized equivalent suffices). It couples S8's prose to S9 without advancing S8.
**Required**: State only what S8 needs: ties are broken arbitrarily and the result satisfies N1/N2 with ⟦Σ̂⟧ = ⟦Σ⟧. Drop the S9 forward pointer; S9 already proves uniqueness independently.

### Issue 4: Defensive justification of a notation choice in S7
**ASN-0053, S7 (CoveringExistence), proof**: "We retain |Σ| = |P| rather than the weaker |Σ| ≤ |P|, since the construction emits exactly one span per position."
**Problem**: This is a paragraph explaining why the bound is stated one way rather than another — meta-commentary on the claim's phrasing, not reasoning that advances it. The construction ("one span per position") already makes |Σ| = |P| evident.
**Required**: Drop the sentence; |Σ| = |P| follows directly from the one-span-per-position construction and needs no defense against the weaker form.

## OUT_OF_SCOPE

### Topic 1: Cross-level intersection and subspace-boundary guarantees
The Open Questions raise intersection at different hierarchical levels and behavior at subspace boundaries. These are genuinely new territory (the level constraint S6 deliberately restricts this ASN to level-uniform spans), correctly deferred — not errors here.

### Topic 2: Span-set difference bound
The final Open Question (tight bound on |normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|) extends S11d to span-sets. Appropriately left for a future ASN; S11d's single-span-pair bound is complete for this note's scope.

VERDICT: REVISE
