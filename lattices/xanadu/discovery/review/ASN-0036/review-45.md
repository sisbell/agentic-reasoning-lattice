# Proof Verification: D-CTG

RESULT: FOUND

**Problem 1 — Missing formal contract.** The property section has no `*Formal Contract:*` block. D-CTG is a design invariant (parallel to S8-fin), so it needs one. The corollary (depth ≥ 3 restriction) is a derived theorem and could also be captured.

**Required:** Add a formal contract. Minimally:
```
*Formal Contract:*
- *Invariant:* `(A d, S, u, q : u ∈ V_S(d) ∧ q ∈ V_S(d) ∧ u < q : (A v : subspace(v) = S ∧ #v = #u ∧ u < v < q : v ∈ V_S(d)))`
- *Axiom:* Every arrangement-modifying operation preserves V-contiguity within each subspace — this is a design constraint enforced by construction, parallel to S8-fin.
```

**Problem 2 — Undeclared dependency on T1(i).** The proof cites "By T1(i)" twice — once for `w > v₁` and once for `w < v₂` — but T1(i) (lexicographic tumbler ordering) is not listed in the Dependencies section. T0(a) and T3 are both declared from ASN-0034; T1(i) should be as well.

**Required:** Add T1(i) to the declared dependencies with its statement (lexicographic ordering: the first component at which two equal-length tumblers disagree determines their order).
