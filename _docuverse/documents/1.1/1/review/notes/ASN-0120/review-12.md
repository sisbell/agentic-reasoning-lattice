# Review of ASN-0120

The proof spine is sound. The V→I confinement argument (T5 + ordinal-displacement ⟹ `t₁ = s_C`), the ML1 coverage equation (`coverage(e_j) ∩ dom(Σ.C) = ρ(R_j,Σ)` via the `#E = 2` store-form), and the ML9 weakest-precondition derivation (Facts (a)/(b), including the `d' = d` boundary where the added link address is inert) all check out. The implementation notes are correctly demarcated as non-normative evidence and are not flagged. The findings below are completeness and anti-bloat items.

## REVISE

### Issue 1: Composite validity is asserted but not verified
**ASN-0120, "The substrate we build on" / "Residence...":** "The link-creation transition is the substrate's `K.λ` ... followed by the link-subspace arrangement extension `K.μ⁺_L`."
**Problem**: MAKELINK is a composite transition. The ASN discharges `K.μ⁺_L`'s *elementary* precondition (ValidComposite★ clause 1) but never addresses clause 2 — the coupling constraints J0, J1★, J1'★ that ASN-0047 requires of every valid composite between initial and final state. A composite is invalid if clause 2 fails; the claim that MAKELINK is realized by this composite is therefore unproven.
**Required**: State (a one-liner suffices) that J0, J1★, and J1'★ hold *vacuously*: MAKELINK allocates no content (`Σ'.C = Σ.C`, ML10) so there is no fresh content address (J0 vacuous) and no content-subspace range-new I-address (J1★/J1'★ vacuous) — only a link-subspace V-position is added.

### Issue 2: V-spec resolution silently excludes ghost/foreign endsets
**ASN-0120, ML6 / ML1**: "the type resolves to stored content like any other endset (`ρ(R₃,Σ) ⊆ dom(Σ.C)`)"
**Problem**: Because every argument is a content-subspace V-spec read through an arrangement, ML1 forces `ρ(R_i,Σ) ⊆ dom(Σ.C)` for *all three* endsets. This makes MAKELINK strictly less expressive than the link model it claims to realize: L9 (TypeGhostPermission) permits type endsets referencing addresses outside `dom(C) ∪ dom(L)`, and L4 (EndsetGenerality) permits endsets referencing any address. MAKELINK-via-V-specs can produce *neither* a ghost type nor any non-content endset. The ASN frames ML6 as establishing "typed relation" in general while silently restricting types to content-backed ones, with no acknowledgement.
**Required**: State the restriction explicitly — V-spec resolution confines every endset (type included) to allocated content, so ghost types (L9) and ghost/foreign references (L4) are not reachable via this operation. (Creating such endsets via a direct-address input mode is legitimately a different operation; mark it OUT_OF_SCOPE if so.)

### Issue 3: ML7 and ML8 assert the same guarantee
**ASN-0120, ML7 / ML8**: ML7 — "`a ∈ dom(Σ''.L) ∧ Σ''.L(a) = Σ'.L(a)`"; ML8 — "The recorded endset value `Σ'.L(a)` is frozen at the creating state."
**Problem**: Both claims are L12 value-fixity. ML8's formal statement is subsumed by ML7 ∧ ML1 (the coverage equation is ML1, the freezing is ML7). The genuinely novel content of ML8 — survivability follows because recording is at I-address identity, not position — is narrative, not a distinct invariant. In anti-bloat terms this is two claims stating one guarantee.
**Required**: Either fold ML8 into ML7, or restate ML8 purely as the survivability *consequence* it uniquely contributes, so it does not re-assert value-fixity.

### Issue 4: Open Question 1 is already answered by the ASN's own claims
**ASN-0120, Open Questions**: "What must MAKELINK guarantee about the relative order in which a single endset's resolved I-address runs are recorded, and is any ordering across runs observable...?"
**Problem**: An `Endset` is `𝒫_fin(Span)` — an unordered set. L5 supplies no span-positional accessor and ML2 (RepresentationIndependence) establishes that span-set representation carries no abstract observable. Within-endset run order is therefore definitionally non-observable; the question is spurious as posed.
**Required**: Remove the question, or reframe it to whatever genuinely remains open (e.g., cross-*slot* ordering, which is fixed by L6 and also not open).

## OUT_OF_SCOPE

### Topic 1: Creating endsets that reference ghost addresses or link-subspace entities
**Why out of scope**: Reaching unallocated addresses or other links requires an input mode other than content-subspace V-specs; this is correctly deferred (OQ3 for the link-subspace case). See Issue 2 — the only in-scope requirement is to *acknowledge* the resulting restriction.

VERDICT: REVISE
