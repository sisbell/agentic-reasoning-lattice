# Review of ASN-0098

## REVISE

### Issue 1: LP19 section bracketed by roadmap preview and closing restatement
**ASN-0098, "Boundary and Width Behaviour" (around LP19a/LP19)**: opening — "We separate two claims: first, that fresh allocations cannot enter a tight endset's coverage; second, that the consequent K.μ⁺/K.μ⁺_L step cannot grow the projection by the resulting V-position." Closing — "...tight endsets are immune to absorbing addresses produced by subsequent K.α or K.λ. Boundary insertion as a composite (K.α + K.μ⁺) cannot enlarge a tight link's reach."
**Problem**: The opening sentence is a roadmap that duplicates the two labeled lemma statements that immediately follow (LP19a = the first claim, LP19 = the second). The closing paragraph then restates the same two lemmas in prose a third time ("immune to absorbing..." = LP19a; "Boundary insertion ... cannot enlarge..." = LP19). The two labeled claims carry both statements; the preview and recap add no reasoning. This is the forward-reference/roadmap accumulation pattern bracketing a section.
**Required**: Delete the "We separate two claims..." preview. In the closing paragraph keep the substantive clarification "Tightness is a construction discipline, not a structural invariant the system enforces" and drop the two sentences that re-state LP19a and LP19.

### Issue 2: Vague appositive in LP8 statement
**ASN-0098, LP8**: "For any document-registration transition `Σ → Σ'` — K.δ in the `Document(e)` case (ASN-0047), the working frame's document-creation operation — registering a fresh document `d_new`..."
**Problem**: The clause "the working frame's document-creation operation" is undefined editorial apposition ("working frame" is not a defined term in this note) and does not advance the claim — the transition is already fully identified by "K.δ in the `Document(e)` case (ASN-0047)." It is removable noise in a structural slot.
**Required**: Drop "the working frame's document-creation operation"; the K.δ citation alone identifies the transition.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
