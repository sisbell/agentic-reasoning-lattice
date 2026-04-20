# Review of ASN-0081

## REVISE

### Issue 1: D-I frame condition underspecified; S7a/S7b/S7c preservation missing

**ASN-0081, D-I (ContentStoreFrame)**: "The content store is unchanged: `(A a ∈ dom(Σ.C) : a ∈ dom(Σ'.C) ∧ Σ'.C(a) = Σ.C(a))`"

**Problem**: The formal statement is S0 (monotonicity — existing entries persist), but the prose says "unchanged" and the registry annotation says "content store unchanged." These are not equivalent: S0 permits `dom(Σ'.C) ⊃ dom(Σ.C)`, while "unchanged" means `Σ'.C = Σ.C`. The weaker S0 formulation leaves the specification underspecified — it admits post-states where new content appears at arbitrary addresses, potentially violating S7a (DocumentScopedAllocation), S7b (ElementLevelIAddresses), or S7c (ElementFieldDepth). These three invariants are not verified anywhere in the ASN.

Compare with D-CD, which correctly uses exact equality: `M'(d') = M(d')`, and D-CS, which gives both domain equality and mapping equality per non-S subspace. D-I should match this strength.

All proofs in the ASN are correct under the weaker D-I — no proof depends on `dom(Σ'.C) = dom(Σ.C)`. The issue is that the invariant preservation section is incomplete: S7a/b/c are system invariants that every operation must preserve, and the current specification does not close the door on violations.

**Required**: (1) Strengthen D-I's formal statement to `Σ'.C = Σ.C` (exact equality as partial functions), matching the prose and the strength of D-CD/D-CS. (2) Add a brief S7-post note in the invariant preservation section: S7a, S7b, S7c are trivially preserved because `Σ'.C = Σ.C` (D-I) implies `dom(Σ'.C) = dom(Σ.C)`, so no new I-addresses exist and the pre-state guarantees carry over unchanged.

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinal depth > 1
**Why out of scope**: The scoping axiom (#p = 2) is explicitly stated as a restriction, and generalization is listed in Open Questions. At depth > 1, TA4's zero-prefix condition becomes non-trivial and TA3-strict's equal-length precondition must be explicitly established — genuine new work, not an omission from this ASN.

VERDICT: REVISE
