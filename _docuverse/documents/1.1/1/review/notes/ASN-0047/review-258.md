# Review of ASN-0047

This ASN is technically dense and largely sound — the transition taxonomy, the two-subspace coupling, the per-state/composite-boundary split, and the worked examples all hold up under checking. The `review-mode.anti-bloat` classifier is present, and the substantive findings below are accumulated meta-prose and duplication, not correctness defects.

## REVISE

### Issue 1: Per-component modification-mode mapping stated three times
**ASN-0047, *Elementary transitions* (closing paragraph), *Temporal decomposition* (table), *Destruction confinement* (P3)**: The closing paragraph of *Elementary transitions* reads "The seven elementary kinds … map to the modification modes per component as follows. (i) *Existential components C, L, E and historical component R* admit only extension (P3) … (ii) *Presentational component M* admits three modes — *extension* … *contraction* … and *bijection-preserving reordering*…". The *Temporal decomposition* table re-encodes the identical mapping (layer → mutability → "Transitions modifying this component"), and P3's prose states the same partition ("The only component that can lose information is M").

**Problem**: Three passages in different sections say the same thing in different words — which transitions touch which component, and that only M contracts. This is the anti-bloat "two paragraphs say the same thing in different words" pattern, compounded to three. A reader following the mode mapping has to reconcile three encodings of one fact.

**Required**: Keep one canonical statement (the *Temporal decomposition* table is the most compact) and reduce the *Elementary transitions* paragraph to a pointer, or delete it — the per-transition effect/frame lines already establish the mapping mechanically.

### Issue 2: P3 packaging restated at four sites
**ASN-0047, *Destruction confinement*, *Extended reachable-state invariants* (twice), *Properties Introduced***: "P3 is the synthesis of P0 ∧ P1 ∧ P2 ∧ L12" (Destruction confinement); "P3 (which packages P0, P1, P2, L12) and content-store invariance…" (ExtendedReachableStateInvariants preamble); "P3 (which packages P0 ∧ P1 ∧ P2 ∧ L12…)" (ExtendedTransitionInvariants); and the same packaging again in the Properties table row for P3.

**Problem**: The fact "P3 = P0 ∧ P1 ∧ P2 ∧ L12" is load-bearing once; restating it at four sites is the same compounding duplication. The "content-store invariance follows from P0 by the arrangement frames" derivation likewise appears in P3's prose and is then re-gestured at in both the ExtendedReachableStateInvariants preamble and ExtendedTransitionInvariants.

**Required**: State the packaging and the content-store-invariance derivation once (in *Destruction confinement*) and have the other three sites cite P3 by name without re-expanding its constituents.

### Issue 3: Forward-pointer scaffolding inside structural enumerations
**ASN-0047, *Elementary transitions* (closing paragraph)**: "The seven elementary kinds — K.α, K.δ, K.λ (introduced later under *Link allocation*), K.μ⁺, K.μ⁺_L (introduced later under *Link-subspace extension*), K.μ⁻, K.ρ…".

**Problem**: A definitional enumeration that pre-announces members defined later, with inline "(introduced later under X)" parentheticals, is navigation scaffolding rather than reasoning. It pairs with Issue 1 — the paragraph both forward-points and pre-states the mode mapping. This is the deferral-accretion pattern the anti-bloat mandate flags.

**Required**: Either move this enumeration after all seven kinds are defined (removing the forward pointers), or drop the parentheticals — the section headings already locate K.λ and K.μ⁺_L.

## OUT_OF_SCOPE

### Topic 1: Link-subspace span decomposition beyond run-cover
S8★(s_L) deliberately omits S8's condition (c) (maximal-run uniqueness) and discharges via the trivial length-1 decomposition. Whether the link subspace warrants a stronger run structure (e.g., whether length-1 link runs are maximal, given link addresses are not in shift-lockstep with V-positions) is a genuine question, but the ASN is explicit that the weaker form is intended, and the relevant invariants downstream (CL-OWN, CL-UNIQ) do not consume (c). This belongs to a future link-ordering ASN, not a revision here.

### Topic 2: ParentAllocatorDispatch constructive recovery of the version parent
In case (b') (fork/version), the owning version allocator's base `d'` is identified existentially ("for some d' ∈ E_doc") rather than by a structural projection from `t`, in contrast to case (a')'s explicit `parent(t)`. Uniqueness is supplied by T10a.6 and the activation premise rides on the minting K.δ event, so the discharge is sound; a constructive recovery formula is a refinement, not a defect in this ASN.

VERDICT: REVISE
