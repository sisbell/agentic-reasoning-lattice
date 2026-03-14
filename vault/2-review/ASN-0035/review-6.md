# Review of ASN-0035

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Account ontology and authorization refinement
**Why out of scope**: The ASN correctly introduces `authorized(actor, p)` as an abstract predicate and defers its refinement. The type of `actor`, the mechanism of authority establishment, and the interaction between DC1 (irrevocable authority) and agent lifecycle are all account-ontology territory. This ASN records the constraint; the next ASN must satisfy it.

### Topic 2: Content resolution semantics for ghost-element references
**Why out of scope**: N0 and N7 establish that spans and links may target empty or unbaptized addresses. What it *means* to resolve such a reference — whether the result is the empty set of bytes, a distinguished "nothing here" value, or a deferred promise — is content-resolution territory, not node ontology.

---

The proofs are sound throughout. Specific observations:

**BAPTIZE freshness derivation** (§ Baptism): Handles both the `C = ∅` and `C ≠ ∅` cases with explicit arguments, ruling out collision with children of the same parent (by TA-strict) and children of other parents (by T3 forcing `parent(m) = p`, contradicting `n ∉ C`). Complete.

**N6 derivation** (§ Structural ordering): The three inter-subtree cases — ancestor precedes descendant (T1 prefix case), all of `Dᵢ` precedes all of `Dᵢ₊₁` (divergence at sibling component), within-subtree by induction — are exhaustive and each direction of the biconditional is covered. The concrete trace correctly demonstrates temporal/structural divergence: `[1,1,1]` baptized after `[1,2]` yet precedes it under T1.

**N8 preservation analysis** (§ Gradual admission): The split between state-dependent invariants (N2–N6, each verified against BAPTIZE) and structural invariants (N9, N10, N16, state-independent from the algebra) is clean. The observation that N6 is derived from N3 + N5 — so preserving those two automatically preserves N6 — is a genuine economy rather than a hand-wave.

**N0 vs N7 scope**: These are complementary, not redundant. N0 establishes content-independence (a baptized ghost element is valid). N7 establishes baptism-independence (an address in `N \ Σ.nodes` is a valid reference target). The extension to permanently unreachable addresses like `[2, 3]` follows from T12's purely arithmetic well-formedness — the system literally cannot distinguish "not yet populated" from "can never be populated" without extra mechanism that would contradict the design.

VERDICT: CONVERGED
