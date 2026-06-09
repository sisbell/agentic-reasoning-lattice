# Review of ASN-0119

## REVISE

### Issue 1: The "precisely when" characterization of footprint fragmentation is a false biconditional

**ASN-0119, "Links" (P7a prose) and "A genuine fragmentation"**: "fragmentation of a contiguous endset occurs *precisely when* a single contiguous run straddles a cut" and "a single contiguous endset becoming discontiguous — occurs *exactly when* a single pre-run straddles a cut." The Claims table P7a row repeats this.

**Problem**: Both statements claim an iff. The necessity direction holds (it follows from P7c by contraposition: not confined ⟹ straddles). But the **sufficiency** direction — a single contiguous run that straddles a cut always fragments — is asserted with only one example and is *false*, refuted by the note's own pivot machinery.

Take the worked pivot `A B C D E ↦ A C D E B` (cuts `ord 2,3,6`, `w_α=1`, `w_β=3`). Let a link cover all of `α ∪ β = {B,C,D,E} = {a₂,a₃,a₄,a₅}`. The pre-footprint `{ord 2,3,4,5}` is a single contiguous run that straddles the cut `c₁ = ord 3`. After the pivot: `M'(ord2)=a₃, M'(ord3)=a₄, M'(ord4)=a₅, M'(ord5)=a₂` — every one of these positions still resolves into the coverage set, so the post-footprint is `{ord 2,3,4,5}` — **still a single contiguous run**. No fragmentation, despite straddling. Because `β` and `α` are relocated to abut and together re-tile `[c₀,c₂)`, a run covering complete relocated regions stays contiguous.

This also produces an internal contradiction: the whole-`α∪β` run is simultaneously "a single contiguous run straddling a cut" (clause 1 says it fragments) and "a footprint split across regions" (clause 2 says the result is indeterminate). The two clauses of P7a disagree on the same input.

**Required**: Weaken "precisely when"/"exactly when" to a necessary-only condition ("fragmentation occurs *only when* a contiguous run straddles a cut"), and state the sufficiency gap explicitly: straddling a cut does not force fragmentation, because a run covering one or more entire relocated region-blocks is re-tiled contiguously. The correct characterization is that a contiguous footprint survives as contiguous exactly when its image under π is again an interval — which holds for within-region confinement (P7c) *and* for runs spanning complete relocated blocks. Provide the argument (or a worked counterexample like the one above) rather than a single fragmenting instance.

### Issue 2: Partiality and degenerate document sizes are never stated

**ASN-0119, "Cuts and regions" / "Well-definedness"**: The note discusses well-definedness only as "the induced map is a bijection of `dom(M(d))` onto itself" — a property of the *post-state given valid input*. It never states which inputs are admissible, nor that REARRANGE is partial.

**Problem**: The boundary cases mandated for an operation are not addressed. An empty text subspace (`V_{s_C}(d) = ∅`), a single-position document, or any document smaller than the affected interval admits no cut sequence satisfying strict ascent + R-PRE(iv) with both moved-region widths ≥ 1. In those cases the operation is simply undefined (ASN-0084 states REARRANGE_K is "partial, defined exactly where R-PRE(K) holds"), but the note never says so. A reader building on this note needs to know REARRANGE is partial and what its domain of definition is.

**Required**: State explicitly that REARRANGE is partial, defined exactly where R-PRE holds, and note the consequence for the degenerate sizes (empty, single-position, sub-interval documents): no valid cut sequence exists, so the operation does not apply — there is no transition.

## OUT_OF_SCOPE

### Topic 1: REARRANGE at V-position depths other than 2, or in subspaces other than `s_C`
**Why out of scope**: The note cleanly restricts itself to the text subspace at depth 2, matching ASN-0084's REARRANGE_K domain, and explicitly disclaims other depths/subspaces. Deeper or link-subspace rearrangement is future territory, not a defect here. No action needed — the scope statement is correct.

VERDICT: REVISE
