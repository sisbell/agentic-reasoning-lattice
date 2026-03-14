# Review of ASN-0036

## REVISE

### Issue 1: S8 ordinal arithmetic introduces notation without citing TA7a (ASN-0034)

**ASN-0036, Span decomposition**: "We write `v + k` for the V-position obtained from `v` by adding natural number `k` to its ordinal component (all other components unchanged)... These are ordinary natural-number additions on a single component — the structural prefix is held as context, not manipulated."

**Problem**: ASN-0034 TA7a defines the ordinal-only formulation for exactly this operation: "a position in subspace S with identifier N and ordinal x is represented as the single-component tumbler [x] for arithmetic purposes, with N held as structural context." The ASN's language ("structural prefix is held as context, not manipulated") is nearly identical to TA7a's ("with N held as structural context"). The ASN introduces `v + k` as a mixed tumbler-plus-natural-number operation without grounding it in the foundation that already formalizes ordinal displacement.

**Required**: Cite TA7a as the foundation for this arithmetic convention. E.g., "Per TA7a (ASN-0034), ordinal displacement within a fixed-depth subspace reduces to natural-number addition on the ordinal component. We write `v + k` for this operation applied to V-positions, and `a + k` for the same applied to the element ordinal of I-addresses." This grounds the notation and lets a reader verify consistency with the foundation.

### Issue 2: S7 cites T5 and T10 for origin uniqueness, but these are insufficient

**ASN-0036, Structural attribution**: "`origin(a) = (fields(a).node).0.(fields(a).user).0.(fields(a).document)` — uniquely identifying the allocating document across the system (by T5 and T10)"

**Problem**: T10 (PartitionIndependence) applies only to non-nesting prefixes. Document prefixes CAN nest — a document with prefix `N.0.U.0.D` and a sub-document with prefix `N.0.U.0.D.d` have nesting prefixes where one extends the other. T10 explicitly requires `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` and says nothing about the nesting case. T5 (ContiguousSubtrees) establishes contiguity of prefix-defined sets but does not establish prefix distinctness. The nesting case is handled by GlobalUniqueness Case 4 (ASN-0034), which uses T10a and T3 to distinguish parent and child allocator outputs by length.

**Required**: Replace "(by T5 and T10)" with a citation that covers all cases. GlobalUniqueness (ASN-0034) is the correct reference — it handles same-allocator (Case 1), non-nesting (Case 2), different zero counts (Case 3), and nesting with same zero counts (Case 4).

### Issue 3: S5 quantifies over "Σ satisfying S0–S3" but S0 is a transition property

**ASN-0036, Sharing**: "`(A N ∈ ℕ :: (E Σ satisfying S0–S3, a ∈ dom(Σ.C) :: |{(d, v) : ...}| > N))`"

**Problem**: S0 is a transition invariant — it relates a state Σ to its successor Σ′. A single state does not "satisfy" a transition property; the phrase is ill-formed. S1 and S6 have the same issue (they govern state pairs). The intent is clear (the invariants impose no finite cap on sharing), but the formal statement is not well-defined.

**Required**: Either quantify over reachable states — "Σ reachable in a system maintaining S0–S3" — or rephrase as a meta-statement about the invariants: "S0–S3 do not entail any finite bound on sharing multiplicity: there is no `N ∈ ℕ` such that S0–S3 together imply `|{(d, v) : v ∈ dom(M(d)) ∧ M(d)(v) = a}| ≤ N` for all reachable states and all `a`."

## OUT_OF_SCOPE

### Topic 1: V-position validity predicate

The ASN defines `M(d) : T ⇀ T` but provides no validity predicate for V-positions analogous to T4 (valid addresses) or S7b (element-level I-addresses). S8-depth constrains depth within a subspace; the worked example uses depth-2 positions (`s.x`). A formal characterization of which tumblers constitute valid V-positions belongs in a future ASN on V-space structure.

**Why out of scope**: The ASN's invariants work with V-positions as given; their internal structure is not needed for S0–S9 to hold.

### Topic 2: Uniqueness of maximal run decomposition

The ASN asks whether the maximal decomposition (fewest runs) is unique. The answer appears derivable — greedy extension of runs is deterministic, so the maximal decomposition is unique — but the proof belongs in a future ASN or addendum on span decomposition properties.

**Why out of scope**: S8 establishes existence of a decomposition; uniqueness of the maximal form is a structural refinement that doesn't affect the invariants.

VERDICT: REVISE
