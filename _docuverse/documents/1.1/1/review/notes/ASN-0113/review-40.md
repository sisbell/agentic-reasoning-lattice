# Review of ASN-0113

## REVISE

### Issue 1: W20 conflates allocated home links with arranged links — the bijection is not surjective onto all home links

**ASN-0113, "Invariants across the members" (W20, FaithfulCount)**: "CL-UNIQ makes `M(d)` restricted to `V_{s_L}(d)` injective — each home link occupies *exactly one* link-subspace V-position — so the correspondence between `d`'s home links and `V_{s_L}(d)` is a bijection and `|V_{s_L}(d)|` counts home links exactly."

**Problem**: CL-UNIQ supplies only injectivity (distinct V-positions map to distinct I-addresses), and CL-OWN supplies only that arranged link positions reference links homed at `d`. Together they give a bijection between `V_{s_L}(d)` and `ran(M(d)|_{s_L})` — the set of links *currently arranged* in `d` — which is a **subset** of `{ℓ ∈ dom(L) : origin(ℓ) = d}`. Surjectivity onto all home links is not established. In the foundation, link allocation (a `dom(L)`-extending step) and link-subspace arrangement (K.μ⁺_L) are distinct transitions; a link can be allocated with `origin(ℓ) = d` yet never placed in `M(d)`. Such a link is a home link of `d` that contributes nothing to `V_{s_L}(d)`. So "each home link occupies exactly one link-subspace V-position" overclaims (it should read "each *arranged* home link"), and "counts home links exactly" is false whenever an unarranged home link exists. This matters because W20 is the claim that the link member is *faithful* to Nelson's "number of links" (W0, 4/68).

**Required**: State the bijection onto `ran(M(d)|_{s_L})` and define the counted quantity as the links *present in `d`'s arrangement*, not all links homed at `d`; or cite a foundation invariant forcing every home link of `d` into `M(d)` (none appears to exist). The content side (S2/S3★) is unaffected and already correct.

### Issue 2: W-pre cites an irrelevant foundation claim

**ASN-0113, "The substrate we measure" (W-pre)**: "(equivalently, by M0/M1 of ASN-0093, `Document(d) ∧ d ∈ dom(M)` ... that some K.δ event has placed into `dom(M)`)."

**Problem**: The stated equivalence (`d ∈ dom(M) ⟹ T4-valid(d) ∧ zeros(d) = 2`) is discharged by M0 alone; M1 (ArrangementMonotonicity) is about non-decreasing `dom(M)` and is irrelevant here. Separately, the parenthetical names "K.δ" (ASN-0047's EntityCreation) while crediting ASN-0093, whose document-registration operation is K.σ — two foundations' vocabularies mixed in one citation.

**Required**: Drop the M1 reference; cite one foundation's registration operation consistently (either ASN-0093's K.σ or ASN-0047's K.δ, not ASN-0093's invariants paired with ASN-0047's operation name).

### Issue 3: the contiguity load-bearing point is restated redundantly (anti-bloat)

**ASN-0113, W4 body, W4 table row, and Open Questions item 1**: the body says "The load-bearing invariant here is contiguity: it is *because* D-CTG★ holds at every reachable state ... that a single half-open span can be exact"; the table row repeats "exactness rests on the standing D-CTG★ contiguity invariant via order-convexity"; the first Open Question opens "W4's single-span exactness rests on the standing D-CTG★ contiguity invariant (see W4)."

**Problem**: The same dependency-on-D-CTG★ observation is asserted in three slots in nearly identical words. The body derivation already establishes the point through D-SEQ★ + T5; the table-note restatement adds nothing, and the Open Question re-explains the dependency before posing its actual (legitimate) forward question. This is the duplicated-statement pattern the anti-bloat classifier targets.

**Required**: Keep the load-bearing role stated once (the body). Reduce the table note to the claim itself, and let the Open Question pose the relaxation scenario without re-deriving the dependency.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
