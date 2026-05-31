# Review of ASN-0093

This note is carrying the `review-mode.anti-bloat` classifier, and that is where the remaining work is. I checked the chain-discipline proofs (FirstEmission, ChainMembershipForOrigin, FirstEmissionFreshness), the C1c/L1c chain exhibitions, the cross-document disjointness lemma, and the worked example against the discharge matrix — the correctness argument holds, including the simultaneous-induction handling of the K.α/lemma circularity and the zero-count boundary on the anchor construction (`zeros(d)=2` exactly satisfies the `k=2` side condition). The findings below are all meta-prose / duplication.

## REVISE

### Issue 1: C1b invariant body carries discharge rationale duplicated by the matrix
**ASN-0093, Content store invariants / C1b**: "Because `E(·)` is T4b's structural projection on the address alone (ASN-0034), depending on no state component, any transition that holds the store in frame leaves the keys unchanged and so transfers each prior key's `#E ≥ 2` unchanged; the same holds for L1b on the link side."
**Problem**: This is a frame-preservation *discharge* argument sitting inside the invariant *statement* slot. The discharge matrix already carries it ("**C1b** … Preserved: `C` in frame (`E(·)` structural — see C1b)") and even back-points to C1b, so a reader following the matrix is bounced to the invariant body and back. The invariant statement is `(A a ∈ dom(C) :: #E(a) ≥ 2)`; the rest is prose to skip.
**Required**: State the invariant only; keep the structural-frame argument solely in the matrix (and delete the matrix's "see C1b" back-pointer along with it).

### Issue 2: L1c/C1c statements forward-reference the same downstream location the matrix already points to
**ASN-0093, L1c**: "The L1c chain exhibition below establishes all clauses of this form at every K.λ event."
**ASN-0093, discharge matrix, C1c**: "Discharged at new key via the T10a-conforming step sequence (see *C1c chain exhibition* below …)"
**Problem**: Both the invariant statement and the matrix forward-point to the chain-exhibition section — two paragraphs deferring to one downstream location. The pointer in the L1c/C1c *statement* advances nothing; the matrix→exhibition pointer already routes the reader.
**Required**: Drop the trailing forward-reference sentences from the L1c and C1c statements.

### Issue 3: Scope "Provided" inventory duplicates the Properties Introduced table
**ASN-0093, Scope / "Provided"**: the Operations / Invariants / Sub-allocator chains / Chain disciplines / Transition-indexed lemmas / Derived chain identity bullets.
**Problem**: This is a second enumeration, with sources, of exactly what the *Properties Introduced* table lists — a use-site/citation-surface inventory. It also pre-announces lemmas defined far later ("Derived chain identity: ChainDiscipline … FirstEmission is a further derived lemma"), the forward-reference-accretion pattern.
**Required**: Collapse "Provided" to a one-line scope statement and let the Properties Introduced table be the single enumeration.

### Issue 4: Cross-document disjointness lemma derives chain disjointness twice
**ASN-0093, Cross-document disjointness chain**: "In particular the sub-allocator chains `A_·(d_i) = S(p_i, 1)` are disjoint … the stream-level statement being ASN-0040's B7 (NamespaceDisjointness)."
**Problem**: The lemma derives chain-level disjointness via a full substrate-local T10 anchor-incomparability argument and then re-attributes the identical chain-disjointness conclusion to B7. For chain elements, B7 alone discharges disjointness; only the stronger "every address extending `p₁` differs from every address extending `p₂`" form does independent work (it is what FirstEmissionFreshness's cross-document branch consumes). Two routes to one conclusion.
**Required**: Keep the T10 derivation for the strictly-stronger any-extension claim it is actually used for; cite B7 once for chain-level disjointness without re-deriving, or drop the B7 aside.

### Issue 5: simultaneous-induction framing re-enumerates the discharge tables' grouping
**ASN-0093, Discharge of stated invariants / "Simultaneous-induction framing"**: the two bullets partitioning properties into "chain-indexed" and "transition-indexed."
**Problem**: The load-bearing content is one sentence — the invariants plus ChainMembershipForOrigin/StoreT4Validity/FirstEmissionFreshness are proved by simultaneous induction with the IH being their conjunction (this is what licenses the K.α/lemma circularity). The bulleted re-listing of which properties land in which group restates what the two discharge tables (citations vs. matrix) already separate.
**Required**: Keep the simultaneous-induction / conjoined-IH sentence; drop the group re-enumeration.

## OUT_OF_SCOPE

None — the deferred topics (arrangement mutation, entity stratification, provenance, coupling, withdrawal) are correctly enumerated and not specified here.

VERDICT: REVISE
