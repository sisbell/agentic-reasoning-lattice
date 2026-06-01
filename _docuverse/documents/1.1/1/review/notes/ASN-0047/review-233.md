# Review of ASN-0047

## REVISE

### Issue 1: "Replacement rides the K.μ⁻ + K.μ⁺ skeleton of K.μ~" conflates two distinct composites
**ASN-0047, *Elementary transitions* (mode taxonomy)**: "*Presentational component M* admits three modes — *extension*…, *contraction*…, and *bijection-preserving reordering* (K.μ~…). Replacement — changing which I-address a V-position maps to — also rides the K.μ⁻ + K.μ⁺ skeleton of K.μ~."

**Problem**: K.μ~ is *defined* as range-preserving — its bijection equation `M'(d)(π(v)) = M(d)(v)` forces `ran(M'(d)) = ran(M(d))`, and J3 states "Reordering preserves ran(M(d))." Replacement does **not** preserve the range: the *interior content replacement* and *prior-provenance/first-time-transcluded* worked examples all change `ran(M(d)|_{s_C})` (e.g. `{a₁,a₂}` → `{a₁,aₓ}`, or add a fresh `a₂'`). None of those examples invoke K.μ~ — they are plain K.μ⁻ + K.μ⁺ (+ K.α + K.ρ) composites. Attributing replacement to "the K.μ⁻ + K.μ⁺ skeleton *of K.μ~*" implies replacement is a K.μ~ instance, which it is not (it violates K.μ~'s admissibility clause (ii)/range preservation). The shared two-step elementary skeleton does not make replacement a reordering.

**Required**: State that replacement is a separate K.μ⁻ + K.μ⁺ composite (range-changing), distinct from the named K.μ~ composite which is range-preserving. Drop "of K.μ~" or replace with "the same elementary K.μ⁻ + K.μ⁺ pair that K.μ~ uses, but without the bijection/range-preservation constraint."

### Issue 2: Dangling cross-reference for `max`-well-definedness in K.α / K.λ subsequent emission
**ASN-0047, Class (a) verification prose, *C-fin***: "Its load-bearing role in K.α's subsequent-emission `max`-well-definedness is stated once in the inherited-foundation table entry (see C-fin at *Inherited from foundation*)."

**Problem**: The pointed-to table entry states only `|dom(C)| < ∞` with its base/preservation argument — it says nothing about `max`-well-definedness. Meanwhile the K.α and K.λ subsequent-emission clauses write `a = inc(max{a' ∈ dom(C) : origin(a') = d}, 0)` and `ℓ = inc(max{ℓ' ∈ dom(L) : origin(ℓ') = d}, 0)` with no on-site discharge of why the `max` exists. The `max` over a tumbler set is well-defined only from finiteness (C-fin/L-fin) **and** non-emptiness (the subsequent-emission predicate) **and** the total order T1 — none of which is assembled at the cite, and the cited target lacks the claimed content. The cross-reference is dangling.

**Required**: Either add the one-line discharge at K.α/K.λ (`max` well-defined: nonempty by the subsequent-emission predicate, finite by C-fin/L-fin, totally ordered by T1), or actually place that statement at the table entry the prose points to. As written, the load-bearing justification is asserted to exist somewhere it does not.

### Issue 3: Forward-reference accretion — repeated deferrals to "V-position depth (operational)"
**ASN-0047, K.μ⁺ precondition, K.μ⁺_L precondition, and *Link-subspace extension* opener**: K.μ⁺ says `m_C(d)` "is governed by the live-depth rule stated above under *V-position depth (operational)*"; K.μ⁺_L's depth bullet says "(defined under *Elementary transitions*, *V-position depth (operational)*)"; the *Link-subspace extension* section opens "The live-depth rule `m_S(d)` governing both subspaces is stated under *Elementary transitions* (*V-position depth (operational)*); we apply it here at `S = s_L`."

**Problem**: Three separate sections defer to the same single definition site for `m_S(d)` without adding content — the pattern flagged under *Forward-reference accretion* ("multiple paragraphs in different sections defer to the same downstream location"). The opener sentence in particular advances no reasoning; it restates the deferral before the substantive K.μ⁺_L use.

**Required**: Cite `m_S(d)` by name at point of use and delete the standalone deferral sentences. One definition site plus bare name-references suffices.

## OUT_OF_SCOPE

### Topic 1: Link inheritance under forking
**Why out of scope**: The fork (J4) leaves the forked document's link subspace empty and explicitly defers "a mechanism for link inheritance under forking" to a future ASN. This is correctly bounded — the Open Questions already capture it; no revision needed here.

### Topic 2: Concurrency / serialization of allocation
**Why out of scope**: SequentialTransitionAxiom assumes atomic, totally-ordered transitions; concurrent same-document allocation is listed in Open Questions. New territory, not a defect.

VERDICT: REVISE
