# Channel Assignment — ASN-0120 review-1

**Date:** 2026-06-08 18:52

## Issue 1: Exact coverage equality `coverage(eⱼ) = ρ(Rⱼ, Σ)` is false as stated
Reason: Internal fix. The weakening to covering (`⊇`) plus content-restriction equality follows directly from ASN-0053 S7 (CoveringExistence) and S3 referential integrity, both already cited; no design intent or implementation evidence is required.

## Issue 2: ML9 wp derivation skips two cases
Reason: Internal fix. Both missing facts — the coverage/`ρ` collapse via `ran(M) ⊆ dom(Σ.C)` and the `d'=d` subspace disjointness (`a ∈ s_L`, content in `s_C`) — are derivable from foundations (S3, SubspaceConventionAxiom) and the operation's own K.μ⁺_L definition already present.

## Issue 3: Missing operation precondition forcing a non-empty type resolution
Reason: The non-emptiness requirement (L3) is settled, but what MAKELINK does when a supplied type *resolves* empty is an operational-behavior question best confirmed against the implementation.
Gregory question: When CREATELINK's type endset argument resolves (via vspanset2sporglset) to an empty sporgl set, does the implementation reject the call, and if so how — or does it guarantee the type spec can never resolve empty?

## Issue 4: ML2 fragmentation claim is non-observable (drift to representation)
Reason: Internal fix. ASN-0098 LP21 (RepresentationInvariance) and ASN-0043 L5 — both already cited — establish span-set cardinality is non-observable, so the restatement to an observable `ρ`-recovery guarantee is derivable.

## Issue 5: `ρ` reinvents ASN-0058's `resolve`
Reason: Internal fix. ASN-0058's `resolve` is already a cited foundation; redefining `ρ` as its union over the spec-set, and naming the `v ∈ dom(M)` filter as a deliberate generalization, is purely an editorial reconciliation.

## Issue 6: Non-foundation cross-ASN reference
Reason: Internal fix. Removing the ASN-0118 dependency and inlining the V-span well-formedness conditions this ASN actually uses requires only the ASN's own content; no external channel informs which foundations are admissible.

## Issue 7: No concrete worked example
Reason: Internal fix. The scenario verifying ML0/ML1/ML9 can be constructed entirely from the ASN's own definitions (ρ, freshness, the discoverability biconditional) and cited foundations; no design intent or implementation evidence is needed.
