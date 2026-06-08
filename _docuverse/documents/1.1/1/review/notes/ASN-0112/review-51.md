# Review of ASN-0112

I checked the construction (`origin_d = min O(d)`, `reach_d = shift(max O(d), 1)`, `extent_d = reach_d ⊖ origin_d`) and the V2 case split against the foundation contracts. The mathematics is sound: the divergence bound `k ≤ #origin_d` is correctly discharged in both the single-subspace (equidepth via S8-depth) and cross-subspace (`k=1`) cases; D0/D1 are applied with their preconditions met; the worked variant's `r⋆ = [2,2,0]` overshoot matches V2's case-2 reasoning; and V-LevelUniform's TA2 citation (`#extent_d = max(#origin_d, #reach_d)`) is correct. The proofs hold. The remaining issues are anti-bloat (the note's classifier), not correctness.

## REVISE

### Issue 1: V15 records a property true of every value, not of this operation
**ASN-0112, "Independence, permanence, and stability" (V15)**: "a span returned at state Σ continues to denote the bounds it denoted then; a later edit to `d` … does not retroactively alter the already-returned value. A subsequent report against the edited state is a *fresh* query, not a mutation of the old answer."
**Problem**: A returned span-set is a value; its denotation `⟦σ⟧` is fixed by its tumblers. "A value does not mutate when state later changes" is definitionally true of *every* query result in the model and is already guaranteed by V-frame's purity (`Σ' = Σ`). The paragraph does not characterize RETRIEVEDOCVSPAN — it restates that the result is a value. This is the "essay content / no reasoning advanced" pattern. V16 (determinism via enfilade confluence) is the substantive, operation-specific half and should be retained.
**Required**: Remove V15, or fold its one non-trivial point (the result is a snapshot, not a live view) into a clause of V16, without a standalone numbered claim.

### Issue 2: V11's closing sentence restates the empty case already established
**ASN-0112, V11**: "So the only sense in which the origin can fail to coincide with occupied content is the empty case, where there is no content to coincide with and no origin at all — and that case is answered with `⟨⟩`, not refused."
**Problem**: The paragraph has already stated that `origin_d = min O(d)` is undefined when `O(d) = ∅` and that the result is `⟨⟩`. This trailing sentence re-says it in different words — the "two paragraphs/sentences say the same thing" pattern at sentence scale.
**Required**: Delete the sentence; V11's content is complete without it.

### Issue 3: deleted/shared-content permanence is re-litigated across three sections
**ASN-0112, V4, V13, V14**: V4 invokes Nelson 4/11 ("may remain included in other versions") for "deleted-but-stored content contributes nothing"; V14 quotes 4/11 again ("those bytes remain in all other documents where they have been included"); V13 makes the transclusion-counts point.
**Problem**: The same 4/11 deletion-permanence material is paraphrased in two separate sections (V4 and V14). The distinct formal claims (V4: absent-from-arrangement content is excluded from extent; V14: occupied positions map to permanent store) do not each need the full Nelson restatement.
**Required**: Cite the 4/11 permanence point once and reference it from the second site, rather than re-quoting.

## OUT_OF_SCOPE

The ASN respects its scope boundary: V5/V6 reason about subspaces only to characterize the *whole-document* span, not per-subspace reporting (ASN-0113), and the Open Questions correctly defer version-comparison and per-subspace-extent topics rather than defining claims for them. No out-of-scope claim definitions found.

VERDICT: REVISE
