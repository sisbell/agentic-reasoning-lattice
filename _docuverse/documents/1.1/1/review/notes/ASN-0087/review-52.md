# Review of ASN-0087

This ASN is technically mature — the composite decomposition, precondition reduction, wp analysis, and invariant sweep all hold up under checking, and edge cases (empty endsets, first-link vs. subsequent placement, reflexive coverage, orphan/resurrection) are handled. My findings are confined to the anti-bloat patterns the `review-mode.anti-bloat` classifier flags: meta-prose and defensive justification accreted around the forward references.

## REVISE

### Issue 1: Use-site inventory and downstream-naming around M-FreshExcl
**ASN-0087, Inputs (Fresh-address exclusion)**: "We state the exclusion generically, so that both the home-link use here and the prior-link reuse in *Side Effects on Prior Links' Discoverability* are instances of one stated form." ... "We cite this derivation downstream as M-FreshExcl."
**Problem**: This is a use-site inventory — it enumerates M-FreshExcl's two downstream consumers and announces the citation rather than advancing the claim. The generic statement (`x ∉ coverage(e)` for fresh `x` under StandardAuthoring) plus its one-line derivation stand on their own; the "so that both... are instances of one stated form" and "We cite this downstream" framing is the kind of cross-section deferral prose that compounds across cycles.
**Required**: State M-FreshExcl and its derivation; drop the consumer inventory and the self-referential naming announcement.

### Issue 2: "Why the definition is shaped this way" prose around StandardAuthoring
**ASN-0087, Inputs (Standard authoring)**: "We intersect coverage with `F` ... *because* `coverage(e)` is infinite while the stores are finite (C-fin, L-fin), so unrestricted `coverage(e) ⊆ dom(Σ.C) ∪ dom(Σ.L)` would be vacuous; `F` is the only set K.α and K.λ allocate from..."
**Problem**: This explains why the definition is needed (refuting a rejected alternative formulation as "vacuous") rather than stating what it means. It is the definitional analogue of "why the axiom is needed" prose.
**Required**: Give the StandardAuthoring definition directly. If the finiteness contrast must be retained, compress to a parenthetical; remove the rejected-alternative argument.

### Issue 3: Defensive exclusion of a wrong derivation route
**ASN-0087, Inputs (Fresh-address exclusion)**: "To do so we must establish `ℓ ∈ F` — and *not* by LP-Sub, whose inclusion `dom(Σ.C) ∪ dom(Σ.L) ⊆ F` (ASN-0098) ranges only over already-stored addresses and so says nothing about the fresh `ℓ ∉ dom(Σ.C) ∪ dom(Σ.L)`. Instead: ..."
**Problem**: Defensive justification — the prose imagines a reader applying LP-Sub, then refutes it, before giving the actual (structural) derivation. The correct derivation (`ℓ` is an `A_L(d)` emission → form `[d,0,s_L,k]` → F's definition) is self-sufficient and needs no contrast against the rejected path.
**Required**: Give the structural derivation directly. Drop the "and not by LP-Sub, whose ... says nothing about" refutation.

### Issue 4: Protocol-rationale essay in Atomicity
**ASN-0087, Atomicity**: "If this intermediate visibility is undesirable — if MAKELINK must appear as a single event — the protocol layer above must enforce it, typically by sequencing both atomic transitions within a single request-response cycle. Composite-level atomicity is thus a protocol-layer guarantee, not a substrate-level one."
**Problem**: The load-bearing system guarantee is "the composite is not atomic at the substrate level" (already stated, and proven via the reachable `Σ_mid`). The remainder is protocol-layer essay content — speculation about how a higher layer "typically" remedies this — which sits in an abstract-spec slot it does not belong in.
**Required**: Keep the substrate-level non-atomicity guarantee and the `Σ_mid` characterization. Cut the protocol-remediation essay, or reduce to a single clause noting atomicity is not a substrate guarantee.

### Issue 5: Reachability-justification prose in Atomicity
**ASN-0087, Atomicity**: "`Σ_mid` is a fully reachable state, not a transitional artifact: by SequentialTransitionAxiom (ASN-0093), K.λ commits before K.μ⁺_L begins, so K.λ on `Σ` yields a complete state `Σ_mid` against which K.μ⁺_L's precondition is evaluated."
**Problem**: This defends the document's own framing ("not a transitional artifact") rather than advancing a claim. The substantive content — `Σ_mid` exists, K.λ commits before K.μ⁺_L, the discoverability delta equals the `Σ → Σ'` delta — is carried by the surrounding sentences. The "fully reachable, not a transitional artifact" defense is meta-prose.
**Required**: State that K.λ commits to `Σ_mid` before K.μ⁺_L is evaluated; drop the "not a transitional artifact" defensive framing.

## OUT_OF_SCOPE

(none — the Open Questions correctly defer forward topics without smuggling them in as claims.)

VERDICT: REVISE
