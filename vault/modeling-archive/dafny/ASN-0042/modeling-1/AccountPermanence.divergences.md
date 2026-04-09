# Divergences — Corollary (AccountPermanence)

- **Line 82**: The ASN states AccountPermanence as a trace-level inductive property over reachable states, but the full induction over state traces is not mechanized. Instead, four structural lemmas are verified that together establish the delegation chain cannot escape dom(π): base case disjointness (BootstrapDomainsDisjoint), structural consequence (EffectiveOwnerExtends), inductive kernel (DelegatorWithinDomain), and single-transition composition (AccountPermanence).
