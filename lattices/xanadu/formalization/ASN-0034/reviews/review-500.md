# Regional Review — ASN-0034/T10 (cycle 3)

*2026-04-24 07:09*

### Index domain attributed to T3 in T10 well-definedness step
**Class**: OBSERVE
**Foundation**: T10 (PartitionIndependence); T0 (CarrierSetDefinition)
**ASN**: T10 proof, well-definedness passage: "Since `k ≤ #a`, `k` lies in T3's index domain `{1, …, #a}`."
**Issue**: T0 — not T3 — introduces the index domain: "the component positions of `a` form the index domain `{j ∈ ℕ : 1 ≤ j ≤ #a}`." T3 merely quotes the range `1 ≤ i ≤ #a` inside its biconditional. Attributing the index domain to T3 points the careful reader at the wrong source, and the `{1, …, #a}` ellipsis notation appears nowhere in the ASN's formal text (T0 writes the set in builder notation). A minor term-ownership slip but a live one because it crosses a citation boundary.

### Expanded prose around the idle `+` operator in NAT-closure
**Class**: OBSERVE
**Foundation**: NAT-closure (NatArithmeticClosureAndIdentity)
**ASN**: NAT-closure body, two paragraphs: "The signature `+ : ℕ × ℕ → ℕ` carries two load-bearing commitments…" through "Totality rules out partial addition and closure rules out sums that escape ℕ." and "The pair `1 ∈ ℕ` and `0 < 1` names a second constant in ℕ and locates it in the strict order."
**Issue**: A previous finding already observes that `+` and the additive-identity axioms do no work in this ASN (only `1 ∈ ℕ` is drawn by T0). These paragraphs expand *further* prose explaining what the idle signature commits to — totality, closure, partial-addition ruled out. When an axiom is already flagged as idle, wrapping it in additional motivational prose is a reviser-drift tell: growing the surface of an unused commitment rather than pruning. The prose is accurate; its presence around an otherwise-idle axiom is the finding.

### Section header paragraphs are orientation prose between claims
**Class**: OBSERVE
**Foundation**: T3 (CanonicalRepresentation); T10 (PartitionIndependence)
**ASN**: "## Canonical form" paragraph: "Equality of tumblers must mean component-wise identity." "## Coordination-free uniqueness" paragraph: "The tumbler hierarchy exists so that independent actors can allocate addresses without communicating."
**Issue**: Both sit between claims as section intros. The first sentence is effectively the T3 conclusion in normative voice ("must mean") — the reader meets the claim's conclusion before its derivation. The second is motivational framing for T10 that does not feed the proof. Neither is meta-prose around an axiom, but both occupy structural slots without carrying formal content; they prime the reader with the conclusion rather than grounding it.

### `k ≤ ℓ ≤ min(m, n)` chains ≤ where `ℓ = min(m, n)` by let
**Class**: OBSERVE
**Foundation**: T10 (PartitionIndependence)
**ASN**: T10 proof: "and `k ≤ ℓ ≤ min(m, n)`."
**Issue**: `ℓ` is defined by `let ℓ = min(m, n)`, so `ℓ ≤ min(m, n)` collapses to `ℓ ≤ ℓ` — true but vacuous. The chain should be `k ≤ ℓ = min(m, n)`. A precise reader momentarily looks for a second inequality that is not there. Correct as written under `≤`-reflexivity, so OBSERVE, not REVISE.

VERDICT: OBSERVE

## Result

Regional review converged after 3 cycles.

*Elapsed: 1590s*
