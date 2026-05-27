# Review of ASN-0091

## REVISE

### Issue 1: P4a verification framing in admissibility section

**ASN-0091, "Worked Example" admissibility verification (both 3-cut and 4-cut)**: "All other foundation invariants — P0, P1, P2, P3, P6, P7, P7a, P8, P4a, NodeLineage, L0–L14, L12, L-fin, C0–C2, C-fin — depend only on state components (Σ.C, Σ.L, Σ.E, Σ.R, dom(Σ.M)) preserved verbatim by RA-frame and so hold at Σ' by direct frame inheritance."

**Problem**: P4a (HistoricalFidelity) is `(A (a, d) ∈ R :: (E Σ_k in transition history : (E v ∈ dom(M_k(d)) : ...)))`. The outer quantification ranges over R (a state component), but the existential witness `Σ_k` ranges over *transition history*, not the current state. The blanket phrase "depends only on state components" is incorrect for P4a — it depends on R *and* on the transition history. The argument for P4a is more subtle than direct frame inheritance, even though the conclusion is correct.

**Required**: Either (a) separate P4a from the "state components only" group and supply its history-aware justification explicitly — R is preserved by RE-R, the pre-REARRANGE history is unchanged, so any pre-existing witness `Σ_k ∈ {Σ_0, ..., Σ_n}` for `(a, d) ∈ Σ.R = Σ'.R` remains valid in the extended history at Σ' — or (b) widen the framing to "state components and historical witnesses preserved verbatim" and note explicitly why REARRANGE leaves both untouched.

### Issue 2: Worked examples don't exercise content-subspace exterior under R-EXT

**ASN-0091, "Worked Example" and "Worked Example — 4-cut Swap"**: Both examples use cut sequences with `c₀ = [1, 1] = min(V_S(d))` and `c_{n-1}` just past `max(V_S(d))`. The affected range therefore covers all of `V_S(d)`, leaving no content-subspace V-positions outside the affected range.

**Problem**: R-EXT (from ASN-0084) is the clause governing V-positions in `V_S(d)` with `v < c₀ or v ≥ c_{n-1}`. Neither worked example actually exercises this case — R-EXT is vacuous in both. The pointwise behavior of R-EXT on content-subspace exterior positions is therefore not concretely verified anywhere in the ASN. The non-S subspace handling is exercised via the link-subspace V-position `[2, 1]`, but that path goes through R-FRAME-P/S(a) and RE-sub, not through R-EXT.

**Required**: Add a third concrete trace (or extend one of the existing ones) with a cut sequence interior to `V_S(d)` — e.g., pre-state with `V_S(d) = {[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]}` and cuts `([1, 2], [1, 3], [1, 5])` so that `[1, 1]` lies in the left exterior and the cut sequence properly tests R-EXT's pointwise preservation of content-subspace positions outside the affected range.

## OUT_OF_SCOPE

### Topic 1: Cross-document transclusion split-by-cut semantics
**Why out of scope**: The first Open Question raises this; it concerns guarantees when a cut splits a single transcluded span into two non-contiguous pieces, which is a refinement of the existing RE-trans for fragmenting transclusions and is appropriately deferred to a future ASN.

### Topic 2: Link-subspace rearrangement semantics
**Why out of scope**: The second Open Question flags this; the current ASN cleanly handles link-subspace as preserved-verbatim (CS3 fixes cut subspace at s_C), and link-subspace cut sequences would be a distinct operation requiring its own definition.

### Topic 3: Observational equivalence at link-discoverability level
**Why out of scope**: Third Open Question; this is a quotient relation on REARRANGE transitions, a derived study rather than a property of the operation itself.

### Topic 4: Upper bound on cardinality increase per invocation
**Why out of scope**: Fourth Open Question; combinatorial bound study, distinct from the existence claims RE-frag/RE-coal/RE-eq the current ASN establishes.

### Topic 5: Compositional realizability of bijections
**Why out of scope**: Fifth Open Question; reachability characterization of the cut-sequence subclass within the abstract Vstream-only class, a future investigation.

VERDICT: REVISE
