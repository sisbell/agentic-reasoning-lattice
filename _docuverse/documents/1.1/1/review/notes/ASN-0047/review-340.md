# Review of ASN-0047

I checked the transition definitions, the K.δ case-split discharges (FrontierEquivalence / ChildSpawnFreshness / ParentAllocatorDispatch), the K.μ~ admissibility/decomposition machinery, the D-SEQ★ derivation (both m=2 and m≥3), S8★'s two-route construction, the Class (a)/(b) verification matrices, and the worked examples. I could not find a substantive correctness gap: invariant coverage is complete, the boundary cases (empty subspace, singleton runs, full clearance, duplicate-I-address fork, interior replacement) are each exercised, and the composite-boundary vs per-state temporal split is handled consistently. The findings below are accretion/forward-reference issues that the `review-mode.anti-bloat` classifier directs me to surface.

## REVISE

### Issue 1: J1★ is fully pre-stated two sections before its formal definition
**ASN-0047, *Coupling and isolation* (opening paragraph)**: "The K.ρ/K.μ⁺ coupling trigger is range-based, not unconditional: K.ρ must co-occur with K.μ⁺ exactly when K.μ⁺ adds an I-address `a` that is *new to the content-subspace range* of the document — `a ∈ ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C})` — … This is the coupling J1★."
**Problem**: This states the full range-based content of J1★ — including its formal trigger predicate — and names it, but J1★ is not formally defined until *Scoped coupling constraints*. A reader meets the same claim twice. This is the "multiple paragraphs defer to the same downstream location" / pre-stated-claim accretion pattern: the preamble does not advance reasoning beyond what the later formal statement carries.
**Required**: Either replace the opening paragraph with a one-line forward pointer ("the K.ρ/K.μ⁺ coupling is range-based; see J1★ below"), or move J1★'s formal statement here and drop the duplicate. Keep one site, not two.

### Issue 2: The "imposed-not-axiom" status of the couplings is restated across two sections
**ASN-0047, *Scoped coupling constraints* (J1★/J1'★ derivation)** and **ValidComposite★ clause (2)**: the derivation says "We *impose* this as the composite-scoped coupling J1'★ below … (imposition motivated in the preamble above)"; clause (2) then says "The couplings J0, J1★, and J1'★ are *imposed* validity conditions, not axioms of the elementary transition system."
**Problem**: The same rationale — that the couplings are validity conditions rather than derived facts of the elementary system — is argued in both places, with the parenthetical "(imposition motivated in the preamble above)" pointing back at a third site. This is the "prose justifies document ordering / restated rationale" pattern; the reader re-reads the same justification while tracking what `ValidComposite★` actually requires.
**Required**: State the imposed-not-axiom status once (the natural home is ValidComposite★ clause (2), where the validity definition lives) and reduce the derivation-site prose to the wp computation that actually produces J1'★.

### Issue 3: "Link V-position permanence" paragraph is exploratory commentary, not a transition/invariant statement
**ASN-0047, *Link-subspace ownership*, "Link V-position permanence"**: "A withdraw-and-re-add composite … re-seats a link without violating any invariant … Hence the presentational order of arrival in the arrangement layer is mutable (P3): the model permits link re-positioning and does not detect it — clause (v)'s single-K.μ~ fixity does not extend to a lifetime guarantee."
**Problem**: This paragraph reasons about a composite (K.μ⁻ + 2×K.μ⁺_L) that no named operation in this ASN performs, and its substantive content — that K.μ~ clause (v) is per-transition, not a lifetime guarantee — is a one-clause observation wrapped in essay about what "the model permits … and does not detect." The load-bearing fact (clause (v) binds a single K.μ~, link identity is held by L12) is already established at K.μ~ and L12.
**Required**: Compress to the single load-bearing sentence (clause (v) is per-transition; link *identity* permanence is L12, independent of arrangement order), or relocate the re-seating walkthrough to the worked-examples block where concrete composites belong.

## OUT_OF_SCOPE

### Topic 1: Interior link withdrawal with renumbering
The ASN's K.μ⁻ contracts the link subspace by suffix removal only; interior withdrawal with V-position compaction is the implementation's `DELETEVSPAN`, correctly listed as a named operation and deferred in the open questions. Not an error here.

### Topic 2: Provenance for content reached through transclusion chains / link endsets
The content-only scope of R (J-LV: links neither trigger nor witness provenance) is a deliberate design boundary, acknowledged in the open questions. New territory, not a defect.

VERDICT: REVISE
