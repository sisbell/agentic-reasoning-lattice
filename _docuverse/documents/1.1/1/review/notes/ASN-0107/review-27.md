# Review of ASN-0107

## REVISE

### Issue 1: D2 reordering clause resolves the request with the wrong arrangement
**ASN-0107, "Two Anchorings" / D2 (DiscoveryNonMonotonicity), reordering bullet**: "the witnessing bijection `π` carries `Σ'.M(d_q)(v) = Σ.M(d_q)(π⁻¹(v))` ... so `Qᵢ(Σ') = {Σ'.M(d_q)(u) : u ∈ π⁻¹(Wᵢ) ∩ dom(Σ.M(d_q))}`."

**Problem**: This formula is incorrect — it applies `π⁻¹` twice. By definition `Qᵢ(Σ') = {Σ'.M(d_q)(v) : v ∈ Wᵢ ∩ dom}`. Substituting the bijection equation `Σ'.M(d_q)(v) = Σ.M(d_q)(π⁻¹(v))` and reindexing `u = π⁻¹(v)` (so `v ∈ Wᵢ ⟺ u ∈ π⁻¹(Wᵢ)`) yields `{Σ.M(d_q)(u) : u ∈ π⁻¹(Wᵢ) ∩ dom}` — with **`Σ.M`**, not `Σ'.M`. As written, `{Σ'.M(d_q)(u) : u ∈ π⁻¹(Wᵢ)}` expands to `{Σ.M(d_q)(π⁻¹(u)) : u ∈ π⁻¹(Wᵢ)} = {Σ.M(d_q)(w) : w ∈ π⁻²(Wᵢ)}`, a double inverse.

Verified against the note's own worked example: there `W₁ = {v₁}`, `π` transposes `v₁,v₂`, and the direct computation gives `Q₁(Σ') = {Σ'.M(d)(v₁)} = {a₂}`. The note's general formula gives `{Σ'.M(d)(u) : u ∈ π⁻¹({v₁})} = {Σ'.M(d)(v₂)} = {a₁} ≠ {a₂}`. The example is correct; the general formula contradicts it.

**Required**: Replace `Σ'.M(d_q)(u)` with `Σ.M(d_q)(u)` in the displayed set (keeping `u ∈ π⁻¹(Wᵢ)`), or leave `Σ'.M(d_q)(v)` and quantify over `Wᵢ` directly. The qualitative conclusion ("need not equal `Qᵢ(Σ)`") is unaffected, but the formula as printed is wrong.

### Issue 2: Set-vs-multiset framing is stated three times
**ASN-0107, "What Is Counted"**: P0's prose ("The point that an implementation is most likely to miss is that this is a *set* cardinality, not a *multiset* tally"), then P1 itself, then the two recap passages ("P1 is the abstract content of the set-versus-multiset decision..." and "P1 says one link is never counted twice; P2 says two links are never counted once. Together they pin the count to set cardinality...").

**Problem**: The same set-not-multiset point is asserted in P0's lead-in, restated as P1, and recapped twice more. This is the "two paragraphs say the same thing" pattern the anti-bloat pass targets; the recaps do not advance the argument beyond the claim statements.

**Required**: Let P1 carry the set-vs-multiset decision once. Drop the anticipatory sentence in P0's prose and collapse the two trailing recap sentences into at most one.

## OUT_OF_SCOPE

### Topic 1: Multi-arrangement (independently-anchored) request parts
R3 and the first Open Question defer the case where `Q₁`, `Q₂`, `Q₃` are anchored to different documents' arrangements. This is correctly deferred — it is new territory (a different resolution discipline), not a defect in the single-arrangement development here.

### Topic 2: Count-vs-retrieval cardinality relationship
The third Open Question raises the relationship between `num` and what FINDLINKS (ASN-0099) would return. This sits on the out-of-scope retrieval operation; it is posed as an open question rather than a claim, so it does not introduce out-of-scope content — acceptable as a pointer.

VERDICT: REVISE
