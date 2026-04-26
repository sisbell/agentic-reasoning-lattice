# Cone Review — ASN-0034/TS4 (cycle 1)

*2026-04-26 10:39*

Reading through the ASN as a system. Checking proofs walk their cases, depends are honored, and prose advances the argument.

I traced ActionPoint's uniqueness/postcondition proofs, TumblerAdd's strict-advancement and dominance case splits (including the `aᵢ = 0 for all i < k` sub-split on `aₖ`), T1's trichotomy/transitivity case grids, and TS4's reduction through OrdinalShift + TA-strict. Components, length, and ordering postconditions all appear discharged. Cross-claim precondition chains (ActionPoint → TumblerAdd → TA0/TA-strict → OrdinalShift → TS4) are unbroken, and dependency lists match symbols actually consumed in proofs.

### NAT-sub use-site inventory paragraph
**Class**: OBSERVE
**ASN**: NAT-sub, the paragraph beginning "The axiom body invokes symbols beyond ℕ's primitive membership..."
**Issue**: The paragraph enumerates, for each cited claim (NAT-order, NAT-closure, NAT-addbound, NAT-addcompat, NAT-zero, NAT-discrete), exactly where its symbols appear in NAT-sub's clauses and consequences, then concludes with "...is declared in the Depends slot accordingly." This is a use-site inventory that duplicates the Depends list — the rubric's named meta-prose pattern. The two strict-monotonicity and strict-positivity derivation paragraphs above already reference these dependencies in proof position; the inventory paragraph adds no inference.
**What needs resolving**: n/a (OBSERVE)

### TS4 dummy `m` is unused in the body
**Class**: OBSERVE
**ASN**: TS4, statement `(A v, n, m : v ∈ T ∧ n ∈ ℕ ∧ n ≥ 1 ∧ #v = m : shift(v, n) > v)`
**Issue**: The dummy `m` is bound only to be aliased to `#v`; it never appears in the matrix `shift(v, n) > v`. The statement is equivalent to `(A v, n : v ∈ T ∧ n ∈ ℕ ∧ n ≥ 1 : shift(v, n) > v)`, with `m` introduced inside the proof when needed for OrdinalDisplacement instantiation. The accompanying paragraph "The dummy `m` abbreviates `#v`..." is then explaining a structural choice rather than carrying inference.
**What needs resolving**: n/a (OBSERVE)

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 1110s*
