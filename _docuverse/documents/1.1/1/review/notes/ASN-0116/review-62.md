# Review of ASN-0116

This is a carefully built note. The two-layer split (immutable I-addresses vs. fluid V-positions) is exploited consistently, INSERT is correctly exhibited as a valid ASN-0047 composite (so the post-state invariants are inherited rather than re-proved), the maximality discussion in IP1 is genuinely careful (backward I-merge happens, forward never, with the right reason), and IP6's discoverability wp is the non-trivial weakest-precondition the standard demands — correctly landing on *containment*, not *emptiness*. The worked example exercises the right boundaries (front, append, empty-arrangement-vs-empty-content-region). I verified the index arithmetic, the gapped/filled bridge, the coupling discharge, and the IP4 witness decomposition; they hold. Two gaps remain in the justification chain.

## REVISE

### Issue 1: F-SUB states a set equality its cited lemma does not establish

**ASN-0116, INSERT operation, Frame clause (F-SUB):** "(F-SUB) `(A S' : S' ≠ S : {v ∈ dom(M'(d)) : subspace(v) = S'} = {v ∈ dom(M(d)) : subspace(v) = S'}` and `M'(d)` agrees with `M(d)` there`)` — ASN-0082 **I3-X (PostInsertionCrossSubspaceFrame)**."

**Problem:** The clause asserts a *set equality* on cross-subspace positions, but I3-X delivers only one inclusion. I3-X quantifies over `v ∈ dom(M(d))` and concludes `v ∈ dom(M'(d))` with value preserved — i.e. {old cross-subspace} ⊆ {new cross-subspace} with agreement (the ⊇ side). The reverse inclusion — that `M'(d)` introduces *no new* cross-subspace position — is ASN-0082's *separate* lemma I3-CX (PostInsertionCrossSubspaceClosure, `(A v : v ∈ dom(M'(d)) ∧ subspace(v) ≠ S : v ∈ dom(M(d)))`), which is never cited anywhere in this ASN.

This missing inclusion is load-bearing, not cosmetic. RAN reads off "the cross-subspace range is unchanged" from F-SUB's image-set equality `{M'(d)(v) : subspace(v) = S'} = {M(d)(v) : subspace(v) = S'}`; that image equality needs the position-set ⊆ (otherwise extra cross-subspace positions could enlarge the range). RAN then drives J1★ (the clause-2 coupling) and IP6 (the discoverability wp, via `ran(M'(d)) = ran(M(d)) ∪ A_new`). So the uncited ⊆ propagates into both the composite-validity argument and the wp.

Contrast I-DOM, which has the same closure-lemma shape but is *locally complete*: its membership (⊇) direction is supplied by the ASN's own adjacent I-LEFT/I-SHIFT/I-NEW clauses. F-SUB has no analogous local source for its ⊆ direction.

**Required:** Cite I3-CX alongside I3-X for F-SUB, or derive the ⊆ inclusion from the realization the ASN already establishes downstream (the amended K.μ⁺ adds only `subspace(v) = s_C` positions and K.μ⁻ retains the link subspace in full at `n'_{s_L} = n_{s_L}`, so no cross-subspace position is added or removed).

### Issue 2: K.μ⁺ precondition discharge omits the finiteness conjunct

**ASN-0116, "INSERT as a valid composite over the K-vocabulary", the K.μ⁺ step:** "Clause 1 at this intermediate state: (i) … (v) …"

**Problem:** ASN-0047's K.μ⁺ precondition includes "`dom(M'(d))` is finite" (and the amendment adds restrictions, it does not drop this conjunct). The (i)–(v) enumeration — presented as the step's complete precondition discharge — never addresses it. It is trivially true (`dom(M(d))` is finite at the intermediate state by S8-fin, and K.μ⁺ adds finitely many positions), but an enumeration offered as *the* precondition check should not silently drop a conjunct, especially given the meticulous per-conjunct discharge elsewhere in the same step.

**Required:** Discharge finiteness explicitly — e.g. extend (v) (which already bounds the content subspace at size `N+n`) by invoking S8-fin for the link subspace at the intermediate state — or cite ASN-0082's I3-fin.

## OUT_OF_SCOPE

No new out-of-scope topics to raise. The four Open Questions (transclusion of a shared insertion point, concurrent insertions without a serializing authority, provenance under transclusion, fragmentation of the inserted run after later editing) correctly fall to future ASNs, and the note raises them as questions rather than smuggling them in as claims. The scope boundary is respected positively: F-LINK (`Σ'.L = Σ.L`) and F-ENT (`Σ'.E = Σ.E`) state INSERT touches neither the link store nor the entity set, so no removal/transclusion/reordering claim intrudes.

VERDICT: REVISE
