## Dependency and Proof Audit

### Global structure

The ASN contains seven definitional/axiomatic claims (Σ.M(d), subspace, S8a, S8-depth, S8-fin, V-sub, D-CTG) and one proof (D-CTG-depth). The proof is the only site where soundness questions arise; the posits are accepted by fiat and are self-consistent in their stated formal contracts. The dependency chain is well-ordered: Σ.M(d) and T0 underlie everything, V-sub carves the subspace, the three posits (S8a/S8-depth/S8-fin) and D-CTG arm the proof.

### Proof trace of D-CTG-depth

The proof proceeds by contradiction: assume two positions in V_1(d) disagree at an interior component j; construct infinitely many distinct intermediates that D-CTG must place in V_1(d); contradict S8-fin's enumerating bijection by a pigeonhole argument (NAT-card upper-bound vs. value-clause). The overall structure is sound. The WLOG u < x step is correctly symmetry-closed; the T1 pinning k = j is correctly derived; the n > u_{j+1} iteration of T0(a) is correctly bounded; the bijection-side counting uses single-valuedness of f rather than its injectivity clause, which is the right primitive. The closing N+1 ≤ N derivation is correct.

---

### [S8a positivity predicate not exported by S8a's Formal Contract]
**Class**: REVISE
**Foundation**: S8a (ArrangementDomainRestriction) — Formal Contract Axiom: `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}`
**ASN**: D-CTG-depth proof body (zeros(w) = 0 discharge) and its Depends entry for S8a:
> "S8a applied to u, whose well-formedness predicate `(A i : 1 ≤ i ≤ #u : uᵢ > 0)` gives u's components their strict positivity directly"
> *(Depends entry)*: "S8a … supplies the well-formedness predicate (`#p ≥ 2 ∧ (A i : 1 ≤ i ≤ #p : pᵢ > 0)`)"

**Issue**: S8a's Formal Contract exports only `dom(Σ.M(d)) ⊆ {t ∈ T : zeros(t) = 0 ∧ #t ≥ 2}`. Applied to u, this gives `zeros(u) = 0`, not `uᵢ > 0`. The positivity predicate `(A i : uᵢ > 0)` is derived in S8a's body using NAT-zero's `(A n ∈ ℕ :: 0 < n ∨ 0 = n)` to rewrite `uᵢ ≠ 0` as `uᵢ > 0`, but that derivation is neither in S8a's Axiom nor in any exported Consequence. D-CTG-depth's proof text cites it as "S8a's well-formedness predicate" — body content presented as a formal-contract export. A formalization tool reading S8a's formal contract would find no such predicate. NAT-zero is absent from D-CTG-depth's Depends, so the conversion cannot be re-derived there either.

The zeros(w) = 0 goal is in fact reachable from the listed Depends via a different path (S8a → zeros(u) = 0; NAT-card bridge → uᵢ ≠ 0; and for n: NAT-discrete + NAT-closure's successor positivity give n ≥ u_{j+1}+1 > 0 → n ≠ 0), but the proof text does not describe this path. Precondition 4 in the Formal Contract exhibits the same mischaracterization, listing S8a as providing `(A i : pᵢ > 0)` rather than zeros = 0.

**What needs resolving**: Either (a) rewrite the zeros(w) = 0 discharge to cite only what S8a's Formal Contract exports — `zeros(u) = 0` via the subset axiom — and use the bridge (already established in the proof via NAT-card) to derive `uᵢ ≠ 0`, which suffices for the goal without NAT-zero; update the Depends entry for S8a and Precondition 4 accordingly; or (b) add a Consequence to S8a's Formal Contract that exports the positivity predicate (S8a's Depends already includes NAT-zero and NAT-card, making it derivable), so that D-CTG-depth's citation is to a formally exported claim.

---

### [NAT-discrete listed in Depends but not consumed]
**Class**: OBSERVE
**Foundation**: NAT-discrete (NatDiscreteness) — Axiom: `m < n ⟹ m + 1 ≤ n`
**ASN**: D-CTG-depth Depends entry for NAT-discrete:
> "the backward direction `j + 1 ≤ m ⟹ j < m` that the w < x branch actually consumes … is not NAT-discrete's but NAT-addcompat's … The w > u branch needs no such conversion, using the additive form `j + 1 ≤ m` directly."

**Issue**: The Depends entry explicitly states that neither branch consumes NAT-discrete's forward axiom (m < n → m+1 ≤ n): the w < x branch uses NAT-addcompat (j < j+1) chained through NAT-order, and the w > u branch reads the interior bound j+1 ≤ m directly. No other proof step (clause-(ii) impossibility, counting argument, enumeration construction) identifiably invokes NAT-discrete's axiom or its no-interval Consequence. The entry reads as though it was written to explain why NAT-discrete is not the source of the key step, yet the entry keeps NAT-discrete on the list — consistent with a stale entry from an earlier proof structure where the w > u branch derived j+1 ≤ m from j < m via the forward direction.

**What needs resolving**: Identify the specific proof step that consumes NAT-discrete's axiom `m < n ⟹ m + 1 ≤ n` or its no-interval Consequence; if no such step exists, remove NAT-discrete from the Depends list.

---

VERDICT: REVISE