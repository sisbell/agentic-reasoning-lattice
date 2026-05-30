# Review of ASN-0043

## REVISE

### Issue 1: L11a recounts GlobalUniqueness's internal proof structure — essay content the reader skips
**ASN-0043, L11a — LinkUniqueness**: "Its precondition is not merely per-event T10a-conformance but that the events are distinct allocation events *within a single system conforming to T10a* — *its proof inducts on one allocator tree, with base case "sole root allocator" and step routing pairs through a lowest common ancestor.* We discharge this by exhibiting one global tree 𝒯..."
**Problem**: The load-bearing content of this passage is exactly two facts: GlobalUniqueness requires a *single-tree* precondition, and we discharge it by exhibiting 𝒯 (via S7d). The recounting of GlobalUniqueness's *internal* induction (base case "sole root allocator," step routing through a lowest common ancestor) advances nothing in L11a's argument — it is a précis of a foundation proof the reader does not need to follow this claim. This is the anti-bloat "essay content in a structural slot" pattern: prose to skip past to reach the discharge.
**Required**: Cut the "its proof inducts on one allocator tree..." clause. State only that GlobalUniqueness's precondition demands a single conforming tree, then give the S7d-based 𝒯 discharge.

### Issue 2: L9's `s_C ≥ 1 / s_L ≥ 1` justification is unused and rests on an existence assumption the precondition does not supply
**ASN-0043, L9 — TypeGhostPermission, *Witness***: "By T4's positive-component constraint on present fields, both `s_C ≥ 1` and `s_L ≥ 1` (each is the first component of some element field, hence non-separator and strictly positive). Choose a subspace identifier `s_X ∈ ℕ` with `s_X ≥ 1`, `s_X ≠ s_C`, and `s_X ≠ s_L`..."
**Problem**: Two defects compound. (i) The facts `s_C ≥ 1` and `s_L ≥ 1` are never used: choosing `s_X` only requires `s_C, s_L` to be defined constants and `s_X ≥ 1` (the latter feeding `g`'s T4-validity), so the sentence advances nothing. (ii) Its justification — "each is the first component of *some* element field" — presupposes that content/link addresses exist, but L9's precondition guarantees only `dom(Σ.M) ≠ ∅`; it admits `dom(Σ.C) = ∅` and `dom(Σ.L) = ∅`, in which case no element field witnesses the claim. Gratuitous prose leaning on an unstated existence assumption.
**Required**: Delete the `s_C ≥ 1 / s_L ≥ 1` sentence; the construction needs only `s_X ≥ 1`, `s_X ≠ s_C`, `s_X ≠ s_L`, all supplied by T0(a) over the fixed constants.

### Issue 3: L0 closing sentence restates the invariant in prose
**ASN-0043, L0 — SubspacePartition**: "`(A a ∈ dom(Σ.L) :: subspace_I(a) = s_L)` … `s_L` is the link subspace identifier introduced by this ASN, and L0 pins every link address to it."
**Problem**: The trailing sentence says exactly what the formula above it already says ("pins every link address to `s_L`" = `subspace_I(a) = s_L` for all `a ∈ dom(Σ.L)`). It is a restatement with no added content — the "two paragraphs say the same thing" pattern in miniature.
**Required**: Drop the sentence, or fold any genuinely new content (that `s_L` is *this ASN's* introduced constant) into the one-line definition where `s_C, s_L` are introduced.

## OUT_OF_SCOPE

None. The ASN respects its declared scope; no operation-level or resolution-level claims have crept in.

VERDICT: REVISE
