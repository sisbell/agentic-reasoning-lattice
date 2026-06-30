Reading the foundation statements and tracing each claim's formal contract against its Depends list.

---

**Structural audit summary.** The NAT-* axiom chain, T0, T1, Σ.M(d), S8-depth, S8-fin, NAT-induction, V-sub, and D-MIN form a coherent dependency order. D-MIN's least-index existence proof is well-structured: P(0) holds vacuously (empty index segment admits no non-empty Q), the step P(N) → P(N+1) splits on Q⁻ correctly, the trichotomy decision at the boundary index covers all three T1 cases, and the mixed-chain closure is handled correctly in both sub-cases. Uniqueness via exactly-one trichotomy is sound. The non-derivability witness {[1,5],[1,6],[1,7]} is valid against D-CTG, S8a, and S8-fin. NAT-induction's relation to well-ordering is correctly stated.

One defect found.

---

### `subspace` Depends missing NAT-closure and NAT-order for `1 ≤ #v`

**Class**: REVISE
**Foundation**: S8-fin (FiniteArrangement), which explicitly establishes the convention; NAT-closure (NatArithmeticClosureAndIdentity); NAT-order (NatStrictTotalOrder)
**ASN**: `subspace` (VPositionSubspaceIdentifier), Formal Contract — Definition: *"For any tumbler `v ∈ T` with `1 ≤ #v`, `subspace(v) = v₁`"*; Depends rationale: *"Writing the guard with the `≤` that already bounds T0's index domain keeps it within the vocabulary T0 supplies, so the relation symbol need not be charged to a separate order foundation; these remain the two foundation symbols the definition consumes — the projection and the length operator."*
**Issue**: The formal contract writes `1 ≤ #v` as a first-class condition in its Definition. This proposition contains two symbols — the constant `1` (requiring `1 ∈ ℕ` from NAT-closure) and the relation `≤` on ℕ (requiring NAT-order) — that T0 does not export. The `subspace` Depends cites only T0 for both, on the argument that the guard is "T0's index-domain condition at j=1." That argument is directly refuted by S8-fin's own statement of the convention: *"T0 uses this same lower bound `1` in its own index domains but grounds it through T0's own dependence on NAT-closure rather than exporting it; the axiom writes `1` as a first-class constant, so it is grounded here directly."* T0's postconditions are the carrier `T`, the length operator, the component-projection signature, comprehension, and extensionality; `1 ∈ ℕ` and `≤` on ℕ are T0's inputs from NAT-closure and NAT-order, not its outputs. A claim that writes these symbols first-class in its formal statement must cite their founding claims directly. The `subspace` prose constructs an exception for itself that contradicts the ASN's own stated rule.
**What needs resolving**: Add NAT-closure (for `1 ∈ ℕ`, the lower bound written into the depth guard) and NAT-order (for `≤`, the relation that bounds the index domain) to `subspace`'s Depends, with rationale matching the pattern S8-fin and T0 use. Remove the "relation symbol need not be charged to a separate order foundation" argument, which contradicts the convention S8-fin establishes.

---

VERDICT: REVISE