# Divergences — Reachable-state invariants (ReachableStateInvariants)

- **Line 9**: S2 (injectivity) is structural — map<Tumbler, Tumbler> is a function. S8-fin is inherent in Dafny's finite map. S8a/S8-depth are not modeled here (see ArrangementInvariantsPreserved for VPosValid abstraction).
- **Line 78**: ProvDocValid (the d ∈ E_doc part of R ⊆ T_elem × E_doc) is an explicit invariant. The ASN states it structurally on Σ.R. Needed for P7 preservation via J1' + S3.
- **Line 106**: Composite states derived properties as conjuncts rather than deriving them from elementary transition frames. In the ASN, permanence follows from PermanenceFromFrames, arrangement preservation from ArrangementInvariantsPreserved, and P6/P8 preservation from K.α/K.δ preconditions + P1. This formulation is sufficient for induction.
