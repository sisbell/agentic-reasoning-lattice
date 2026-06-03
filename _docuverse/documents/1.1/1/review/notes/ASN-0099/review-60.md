# Review of ASN-0099

I checked the operation definitions, every introduced claim (A1, A1a, F1–F20a, the meta/sub-lemmas), the design-justification witnesses in F4, the cross-document ordering proof F10a, and the worked example for internal consistency.

## Findings

**Operation coverage is complete.** The full transition vocabulary `V = {K.α, K.λ, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.μ⁺_L, K.ρ}` is partitioned: A1a discharges link-store inertness of the six non-allocating atomic ops from their published frames; K.μ~ is reached only through its K.μ⁻+K.μ⁺ decomposition; K.λ is isolated and its delta characterized (F9-λ). The exclusion of ASN-0093's K.σ is justified against M1/P8. No operation is hand-waved.

**Boundary cases are addressed.** Empty `I`, `I=∅`, `R` disjoint from the arrangement, empty link store, empty arrangement, empty constraint set / empty constraint target, empty `S`, empty non-type slots, arity > 3 (existential over all slots), and cross-subspace link-valued images (Query 4) are each handled explicitly.

**The hard proofs hold up.** F10a Case (ii) (version tumblers as proper prefixes of their parent at document level) is genuinely reachable and its zero-count argument is complete (two zeros confined to positions ≤ #d₁−1, terminal nonzero transported, forcing `d₂_{#d₁+1} ≥ 1`). The F4 strengthening/weakening witnesses each correctly exhibit F1-admit / alternative-reject, and the "all slots populated" requirement for Strengthening 1 (to avoid vacuous `∅ ⊆ I`) is correctly identified. The I-side/V-side persistence distinction (F11 vs ASN-0098's `discoverable_from`) is drawn precisely and demonstrated by Query 5's K.μ⁻ contraction.

**Derivations have adequate depth.** F8 grounds on the spelled-out ComprehensionInvariantUnderΣL; F11/F19/F9-λ correctly fall back to the per-link primitive PerLinkInvarianceUnderValuePreservation where `dom(L)` grows under K.λ; F13, F20, F20a chain named identities step by step; a concrete worked example verifies the key postconditions.

The ASN defines state-level operations and their guarantees (completeness, soundness, determinism, survivability, monotonicity, ordering) abstractly, against an unspecified `result` function, with implementation mechanics explicitly deferred. It has not drifted into implementation territory.

I found no correctness error, missing case, unestablished postcondition, missing example, or hand-wave undermining a formal claim. Minor textual incompleteness (e.g., the F17/F18 discharge prose names K.μ⁺/K.μ⁻ but not K.μ⁺_L) is covered by the cited basis F9, which includes all three K.μ-family steps, so no formal claim is affected.

## OUT_OF_SCOPE

The "What We Have Not Specified" and "Open Questions" sections appropriately defer FOLLOWLINK/RETRIEVEENDSETS (inverse direction), replication/partition tolerance, access-control composition, timing bounds beyond "next query after K.λ", and querying I-addresses outside the stores. These are correctly future territory, not defects in this ASN.

VERDICT: CONVERGED
