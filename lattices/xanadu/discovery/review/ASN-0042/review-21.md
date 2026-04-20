# Review of ASN-0042

## REVISE

### Issue 1: O9 quantifies over all T but invokes field extraction that requires T4

**ASN-0042, Node-Locality section**: "O9 (NodeLocalOwnership). `(A π ∈ Π, a ∈ T : owns(π, a) ⟹ N(pfx(π)) ≼ N(a))`"

**Problem**: The statement quantifies over all `a ∈ T`, but `N(a)` is defined via `fields(t)` from T4/T6 in the foundation, which has the explicit precondition `a, b ∈ T` are valid tumblers satisfying T4. For arbitrary tumblers not satisfying T4 (e.g., `[1, 0, 0, 5]` — adjacent zeros), `N(a)` as defined by the foundation is not guaranteed well-defined.

The proof is correct in substance — when `pfx(π) ≼ a` with T4-valid `pfx(π)`, the prefix relation forces enough structure on `a` to extract "components before the first zero" unambiguously. But the formal statement invokes a function outside its defined domain.

Every other property in the ASN that uses field extraction (O6, AccountPrefix, the `pfx(ω(a)) ≼ acct(a)` derivation) correctly restricts to allocated addresses where O17 provides T4. O9 is the sole exception.

**Required**: Either restrict O9's quantification to allocated addresses (`a ∈ Σ.alloc`, where O17 gives T4) or to T4-valid tumblers (`T4(a)`). The proof needs no change — the argument from the prefix relation is correct; only the formal statement's domain needs tightening.

## OUT_OF_SCOPE

(none)

VERDICT: REVISE
