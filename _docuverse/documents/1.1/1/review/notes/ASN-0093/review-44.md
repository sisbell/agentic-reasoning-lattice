# Review of ASN-0093

## REVISE

### Issue 1: SubsequentEmissionFreshness is load-bearing but excluded from the induction
**ASN-0093, Discharge of stated invariants (simultaneous-induction framing) + lemma-preservation matrix**: "The stated invariants, together with the ChainMembershipForOrigin lemma, the StoreT4Validity corollary, and the FirstEmissionFreshness lemma, are proved by *simultaneous induction* over transition sequences from `Σ₀`"

**Problem**: SubsequentEmissionFreshness is omitted from this list, and the lemma-preservation matrix carries rows only for ChainMembershipForOrigin, StoreT4Validity, and FirstEmissionFreshness — no row for SubsequentEmissionFreshness. But SubsequentEmissionFreshness is exactly as load-bearing as FirstEmissionFreshness: it is cited to discharge K.α's and K.λ's subsequent-emit binding preconditions ("Freshness of `a` against `dom(C) ∪ dom(L)` is supplied by SubsequentEmissionFreshness"). Its own proof depends on inductive properties evaluated at the pre-state — ChainMembershipForOrigin (to place `a_prev ∈ A_C(d)` and `a ∈ A_C(d)` and to invoke the contiguous-prefix form) and L0 (cross-subspace bullet: "each peer `a ∈ dom(C)` carrying `E(a)₁ = s_C` by L0"). A per-transition freshness statement that consumes IH-at-`Σ` cannot be treated as state-independent; FirstEmissionFreshness was included in the induction for precisely this reason. The asymmetry is unexplained.

**Required**: Either add SubsequentEmissionFreshness to the simultaneous-induction conjunction and give it a row in the lemma-preservation matrix, or justify in text why it discharges from already-established properties without itself needing to be carried through the induction (and why FirstEmissionFreshness then differs).

### Issue 2: Defensive parenthetical narrates negative space rather than advancing the claim
**ASN-0093, SubsequentEmissionFreshness (cross-subspace bullet)**: "`E(a)₁ = s_C` (read along `A_C(d)` via DisjointSubAllocatorChains — structural, since `a ∈ A_C(d)`; **L0's C-clause cannot supply this, as `a ∉ dom(C)` at the freshness-check point**)"

**Problem**: The bracketed clause justifies why an alternative route (L0) does *not* apply. The claim is fully carried by "DisjointSubAllocatorChains, since `a ∈ A_C(d)`." Explaining which non-chosen lemma fails is meta-prose the reader must work around — a defensive justification of the kind this note's anti-bloat classifier flags.

**Required**: Delete the "L0's C-clause cannot supply this…" clause; the DisjointSubAllocatorChains citation stands alone.

### Issue 3: Repeated same-document deferrals to the same downstream/upstream location
**ASN-0093, intro + K.σ + worked example Steps 1/5/9**: "deferred higher-layer concerns are enumerated under *Deferred to higher-layer ASNs* in Scope" and, four times, variants of "available once `d ∈ dom(M)` (see *Active sub-allocator chains* above)".

**Problem**: The intro forward-points to a section of the same document, and "(see *Active sub-allocator chains* above)" recurs across K.σ and three worked-example steps. Multiple paragraphs deferring to a single location is the accretion pattern this note is asked to surface; the pointer adds no reasoning at any of its sites.

**Required**: Drop the intro forward pointer (Scope already enumerates the deferrals) and the repeated "(see … above)" cross-references; the definition is locatable without per-use signposting.

### Issue 4: Essay analogy embedded in a lemma statement
**ASN-0093, Lemma (ChainMembershipForOrigin)**: "The contiguity matches ASN-0040's B1 (ContiguousPrefix) for the baptismal registry: the content and link sub-allocator chains have the same 'always-extend-by-one-from-the-current-frontier' discipline as Nelson's baptism."

**Problem**: This is commentary that does not advance the lemma's claim or its proof; it sits inside the lemma statement. (The analogy itself is acceptable content per the placement rule — the issue is that it occupies a structural slot where the precise reader must skip it to reach the proof.)

**Required**: Move the analogy to surrounding prose or drop it; the lemma statement should contain only the claim.

## OUT_OF_SCOPE

### Topic 1: Layering relationship between this substrate and ASN-0043/ASN-0036
The note both cites ASN-0043/ASN-0036 as foundations and re-derives their invariants (C0 = S0/S1, C1 = S7b, L0–L12) under its own new operations. Whether the substrate should sit *below* those ASNs (making them depend on it) rather than restating their invariants is an architectural question for the layer-stack design, not a correctness error in this self-contained note.

VERDICT: REVISE
