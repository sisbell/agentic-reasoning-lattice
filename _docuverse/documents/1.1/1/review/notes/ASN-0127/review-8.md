# Review of ASN-0127

I checked every primitive, every derivation, and every step of the worked illustration. The mathematics is sound: F-IMG-SWING's reindexing and its injective/non-injective cardinality witnesses are correct; F-UDIST's unrestricted form is genuinely needed for F-VDIST under content sharing; F-CIL/F-PRES/F-INERT compose correctly; E-INV/E-MONO/E-CONS are airtight; D-NONMONO's case split over the K-vocabulary is exhaustive (μ⁺/μ⁺_L, μ⁻, μ~ on d_q, plus off-document with K.λ the sole mover); D-CWP's `B ⊆ A` derivation is a correct weakest-precondition characterization; and the worked illustration's four motions (K.α inertia, K.μ⁻ shrink, K.μ⁺ store-fixed rise, K.μ~ lateral swing `{L_1}↦{L_2}`) all check out against the stated arrangements, including the admissibility of the transposition reorder and the subtree-coverage slot reductions. Boundary cases (empty region, empty I, fresh document, full clearance `n'=0`, non-injective sharing) are all handled.

I found one defect, and it is notational rather than mathematical.

## REVISE

### Issue 1: The query-region symbol collides with the provenance component of Σ, and is named inconsistently
**ASN-0127, "State and notation" and F-IMG (Phase 1)**:
- State: "We operate over the extended state `Σ = (C, L, E, M, R)` … and provenance relation `R`."
- F-IMG: "For `d ∈ dom(Σ.M)` and `R ⊆ T`: `image(R, d, Σ) ≡ {Σ.M(d)(v) : v ∈ R ∩ dom(Σ.M(d))}`."

**Problem**: The note names the query region `R ⊆ T` — the central free variable of Phase 1, used pervasively (F-IMG, F-IMG-MONO/CONTR/SWING, F-V, F-VDIST, and the worked illustration's `R = {v_1, v_2}`, `R₀ = {v_1}`) — with the exact symbol `R` that it just bound to the provenance relation in the state tuple `Σ = (C, L, E, M, R)`. Reading "`R ⊆ T`" one line after "`Σ = (…, R)`, … provenance relation `R`" forces the reader to resolve an overload on every occurrence. Compounding this, the discovery section names *the same concept* differently: "a query V-region `W ⊆ T`" (D-PRES, D-NONMONO, D-CWP). So the region is `R` in the Phase-1/composite lemmas and `W` in the discovery analysis — a reader must independently realize `R` and `W` denote the same kind of object, and that D-NONMONO's `image(W, d_q, Σ) ⊆ image(W, d_q, Σ')` is just F-IMG-MONO (stated over `R`) instantiated at `W`. This is below the note's own notational standard, which elsewhere goes out of its way to keep symbols apart (`subspace` vs `subspace_I`; the explicit `𝒮` vs `S` care inherited from the foundations).

**Required**: Use a single region symbol that does not collide with the state tuple — `W` is already in use for exactly this purpose in the discovery section, so adopt `W` (or another fresh letter) throughout the Phase-1 and composite lemmas, F-V/F-VDIST, and the worked illustration, retiring `R` as a region name. If `R` is retained for any reason, add an explicit one-line note at first use disambiguating it from the provenance component and unifying it with the discovery section's `W`.

## OUT_OF_SCOPE

### Topic 1: Content-keyed queries naming addresses through Σ.C rather than Σ.M
**Why out of scope**: This is the note's own first Open Question. `image()` is deliberately arrangement-mediated (Phase 1 consults `Σ.M`); a query that names I-addresses directly through the content store is a different primitive with a different stability profile (it would lean on S0/P0 permanence rather than the M-mediated swing analysis). It is correctly deferred — the present note answers "the arrangement-mediated content-region link query, and only that," and that scope is self-consistent.

### Topic 2: Operational composition with ASN-0098's link projection displacement
**Why out of scope**: The note's fourth Open Question. Both `image()` and the LP** results consult `Σ.M`, and "project a link through arrangement, then ask whether the projection meets a content region" is a genuine composite — but it is a composition of two foundations, not a gap in either phase as specified here.

VERDICT: REVISE
