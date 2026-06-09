# Review of ASN-0116

## REVISE

### Issue 1: I-DOM cites a lemma that does not bear on the equation it justifies
**ASN-0116, Effect clause (I-DOM)**: "The left prefix `{q_1, …, q_{J-1}}` and shifted suffix `{q_{J+n}, …, q_{N+n}}` are the gapped domain that ASN-0082 I3-CS/I3-CX characterise (specialised to the dense text subspace)."

**Problem**: I-DOM's equation is explicitly about `{v ∈ dom(M'(d)) : subspace(v) = S}` — the subspace-`S` (text) domain only. The lemma that characterises that domain is I3-CS (PostInsertionSubspaceClosure: `v < p ∧ v ∈ dom(M(d))` or `v = shift(u, n)`). I3-CX (PostInsertionCrossSubspaceClosure) governs positions with `subspace(v) ≠ S` and contributes nothing to this equation. The joint citation "I3-CS/I3-CX" attaches an irrelevant lemma to a subspace-`S` claim.

**Required**: Cite I3-CS alone for the subspace-`S` gapped domain. If the intent was to note that cross-subspace positions are accounted for, say so separately and point to F-SUB / I3-X (the cross-subspace *frame*), not I3-CX, which is the gapped-arrangement's other-subspace *closure*.

### Issue 2: the post-insertion shift values are grounded twice
**ASN-0116, Effect clauses (I-SHIFT, I-LEFT) vs. "INSERT as a valid composite"**: the Effect establishes `M'(d)(shift(v,n)) = M(d)(v)` by citing ASN-0082 I3/I3-L; the composite section then constructs the K.μ⁻ → K.μ⁺ sequence, whose K.μ⁺ step installs `{q_{J+n}, …, q_{N+n}} → {M(d)(q_J), …, M(d)(q_N)}` — i.e. the same values directly — and loops back with "The net effect of K.μ⁻ then K.μ⁺ … is *exactly* I3's post-insertion shift."

**Problem**: The shift values are derived from two sources (the I3 postcondition-spec and the explicit K.μ⁺ contract). Since INSERT's authoritative realization is the K-atomic sequence, the K.μ⁺ construction already pins the values; the I3 citation in the Effect is then a parallel grounding of the identical fact. This is the kind of double-derivation the anti-bloat pass is meant to surface — a reader must reconcile the two framings to confirm they say the same thing.

**Required**: Pick one as load-bearing. Either state the Effect values as *specification* and let the composite section be the sole *proof* (Effect cites forward to the composite, not to I3), or ground entirely on I3 and have the composite section merely assert applicability without re-listing the per-position images. One direction should subsume the other rather than both standing as independent derivations.

## OUT_OF_SCOPE

### Topic 1: transclusion at a shared/transcluded insertion point
The first Open Question (insertion at a position shared by transclusion) is correctly deferred — it belongs to ASN-0118 (COPY/transclusion), not here.

### Topic 2: concurrent insertions and serializing authority
The second Open Question (two concurrent fresh-claiming insertions) concerns multi-authority allocation, outside a single-operation INSERT note.

VERDICT: REVISE
