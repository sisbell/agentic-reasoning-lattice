The ASN presents six local claims (Σ.M(d), subspace, V-sub, S8-depth, S8-fin, NAT-induction) and one proved requirement (D-MIN). I trace each formal contract, check its depends list, and then examine the cross-claim argument in D-MIN's existence proof in detail.

**Σ.M(d), subspace, V-sub.** The type declaration, the first-component selector, and the subspace projection are all correctly stated. V-sub grounds 1 ∈ ℕ directly at NAT-closure rather than routing through T0, matching the cited rationale. The disjointness consequence (each active position belongs to exactly one projection) is correct and trivially follows from subspace being a function; it need not appear in the formal contract.

**S8-depth.** The uniform-depth posit is correctly distinguished from S8a (which restricts dom keys to depth ≥ 2) and from OrdShiftHom (which fixes #shift(v,n) = #v frame-internally). The exclusion of both from the depends list is justified: neither contributes a symbol to #u = #w.

**S8-fin.** The bijection formulation avoids the out-of-scope |·| operator. The base-state witness n = 0 is correctly grounded at NAT-zero (the element 0 in the existential's range), distinct from NAT-closure's lower-bound 1 in the segment. The injectivity clause (A i, j : 1 ≤ i < j ≤ n : f.i ≠ f.j) captures full injectivity via ordered-pair coverage and trichotomy.

**NAT-induction.** The axiom is correctly stated and grounded only in NAT-carrier (ℕ), NAT-zero (0), and NAT-closure (n+1 and closure). Order axioms are correctly excluded — the principle does not use <.

**D-MIN existence proof.** The least-index principle P(N) is properly stated for g : {j : 1 ≤ j ≤ N} → T and non-empty Q ⊆ {j : 1 ≤ j ≤ N}. The induction structure is sound: base P(0) holds vacuously (the index segment {j : 1 ≤ j ≤ 0} is empty, so no non-empty Q exists); step P(N) → P(N+1) is discharged by the Q⁻ = ∅ branch (J = N+1, reflexivity) and the Q⁻ ≠ ∅ branch (IH gives J', trichotomy on g.(N+1) vs g.J' closes both sub-cases). The base N = 0 → P(1) bridge via the Q⁻ = ∅ arm of the step is correctly identified. NAT-induction's predicate-form then delivers P(N) for all N ∈ ℕ. Applying P(N) at g = f (S8-fin bijection, valued in dom(Σ.M(d)) ⊆ T) and Q = Q₀ = {j : f.j ∈ V_1(d)} recovers the minimum. Uniqueness follows from T1's trichotomy in the standard two-least-elements argument. The depends list (V-sub, S8-depth, T0, NAT-closure, T1, NAT-induction, S8-fin) is complete and correctly attributed.

No REVISE-level errors found. Two OBSERVE items below.

---

### NAT-induction forward references omit D-MIN
**Class**: OBSERVE
**Foundation**: NAT-induction (NatInduction)
**ASN**: NAT-induction Formal Contract, Forward References section: lists only D-PRED and D-INJ
**Issue**: D-MIN's existence proof uses NAT-induction as the primary induction engine (the least-index principle P(N) induction), which D-MIN's own depends list correctly records. NAT-induction's forward reference list is therefore incomplete: D-MIN is a downstream consumer of the same standing as D-PRED and D-INJ.
**What needs resolving**: Add D-MIN (VMinimumPosition) to NAT-induction's Forward References, with a note that its role is the least-index existence induction over S8-fin's enumeration length.

---

### D-MIN step-case prose fuses case label with derivation
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder), D-MIN body, "Existence and uniqueness" paragraph
**ASN**: D-MIN, step N → N+1, sub-case N+1 ∈ Q, case g.(N+1) < g.J': *"the mixed chain g.(N+1) < g.J' ≤ g.j closes to g.(N+1) ≤ g.j by T1's transitivity, split on the ≤: g.J' < g.j through pure <-transitivity, g.J' = g.j by rewriting g.(N+1) < g.J' under indiscernibility of ="*
**Issue**: The phrase "g.J' = g.j by rewriting g.(N+1) < g.J' under indiscernibility of =" is grammatically ambiguous: "g.J' = g.j" reads as the conclusion of the rewriting rather than as the case assumption under which the rewriting is applied. The intended reading is: in the sub-case g.J' = g.j (case assumption), substitute g.J' ↦ g.j in g.(N+1) < g.J' by indiscernibility to obtain g.(N+1) < g.j. The logic is correct; the prose mixes case label and justification.
**What needs resolving**: Separate the case label from the justification. One phrasing: "split on g.J' ≤ g.j — case g.J' < g.j: g.(N+1) < g.J' < g.j closes by <-transitivity; case g.J' = g.j: substitute g.J' by g.j in g.(N+1) < g.J' via indiscernibility to get g.(N+1) < g.j."

VERDICT: OBSERVE