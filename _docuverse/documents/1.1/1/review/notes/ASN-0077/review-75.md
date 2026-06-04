# Review of ASN-0077

This note is, on the mathematics, in very good shape: the pointwise projection O0, the two lifts, the permanence/monotonicity chain (O5–O7, O5★/O6★), the K.μ⁺/K.μ⁺_L preservation arc (O11/O11'/O11.1/O11★★) and the negative witnesses (O13/O14) all check out, including the long singleton-I-span squeeze argument and the worked-example witnesses for O13/O14. The findings below are confined to the forward-reference / meta-prose accretion that the `review-mode.anti-bloat` classifier asks me to surface, plus one duplication.

## REVISE

### Issue 1: Proof-plan narration inside the O2 derivation
**ASN-0077, Claim O2 (Block uniformity), derivation**: "*In either subspace case we first discharge the subspace identification at `vⱼ + i`, since S3★ (ASN-0047) — which we will invoke to place `aⱼ + i` in the appropriate I-domain — requires the antecedent `subspace(vⱼ + i) = s_C` (resp. `s_L`).*"
**Problem**: This sentence narrates the *plan* of the proof ("which we will invoke", "we first discharge … since … requires") rather than executing a step. The actual discharge (M-int → subspace agreement → S3★) follows immediately and stands on its own. The planning sentence is meta-prose occupying a proof slot.
**Required**: Delete the planning sentence; let the M-int/S3★ steps carry the argument directly.

### Issue 2: Non-consumer inventory in O3
**ASN-0077, Claim O3 (Structural derivation), V-span paragraph**: "*No further state component (no values from C or L beyond the address itself, no R, no E, no other document's arrangement) is consulted.*" and the parenthetical "*(Codomain typing — `M(d)(v) ∈ dom(Σ.C) ∪ dom(Σ.L)` — is supplied by S3★ (ASN-0047) but not consulted by the computation.)*"
**Problem**: The bracketed enumeration of everything *not* read (`R`, `E`, other arrangements, content values) and the parenthetical naming a fact that is "supplied but not consulted" are use-site/non-consumer inventory. The claim's content is "computed by scanning the value alone"; once that positive statement is made, listing each unconsulted component and each supplied-but-ignored typing fact adds no reasoning.
**Required**: State that `origin(M(d)(v))` is computed from the address value alone; drop the non-consumer list and the "supplied but not consulted" parenthetical.

### Issue 3: Exclusions duplicate the Open Questions
**ASN-0077, "What SHOWORIGIN does not promise" vs. "Open Questions"**: "*Not historical containment … recorded in the provenance relation `Σ.R` … is a separate concern*" restates Open Question 4 ("*Does the system require a complementary operation reporting historical containment (from `Σ.R`) …*"); "*Not transitive provenance. The result names `d₁` …, not the transclusion chain*" restates Open Question 2 ("*must any abstract operation be provided that surfaces the intermediate chain*").
**Problem**: Two of the three exclusions say in scope-boundary form exactly what two of the four open questions say in future-work form — the same fact stated twice in different sections.
**Required**: Keep each concern in one place. Either let the exclusions carry the boundary and drop the twinned open questions, or let the open questions carry them and trim the exclusions to a pointer.

## OUT_OF_SCOPE

### Topic 1: Unified content+link origin operation; intermediate-chain operation; native-vs-transclusion distinction
**Why out of scope**: These are the genuine remainder in the Open Questions (the ones without an exclusion twin). They name operations this ASN deliberately does not provide; they belong to future ASNs, not to a revision of SHOWORIGIN.

VERDICT: REVISE
