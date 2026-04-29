# Review of ASN-0085

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Order preservation under ord within a subspace
**Why out of scope**: The ASN focuses on the additive homomorphism. The natural companion — that ord reflects and preserves the T1 order when restricted to a single subspace (same first component) — is a different property that downstream ASNs can derive from the definitions here plus T1 directly.

### Topic 2: Generalizing OrdAddHom to #w ≠ m
**Why out of scope**: The homomorphism holds whenever `#w ≥ 2`, `w₁ = 0`, `w > 0`, and `actionPoint(w) ≤ #v` — the equal-length condition `#w = m` is sufficient but not necessary, since TumblerAdd's three-region decomposition produces matching component sequences regardless of #w. The current precondition is correct and covers the shift case and all same-depth displacements; a future ASN could generalize if cross-depth displacements arise.

---

The definitions are precise and the proofs are explicit component-by-component constructions — no hand-waving, no proof-by-checkmark. Both instances are well-chosen: (a) exercises the deepest action point (k = m, no tail components — the shift case), and (b) exercises an intermediate action point (k = 2, with a zero tail component that demonstrates the S-membership boundary). The edge cases (k = 2, k = m, m = 2) are all covered by the general TumblerAdd decomposition. The OrdAddS8a biconditional correctly identifies the tail-component positivity as the sole condition, and OrdShiftHom correctly invokes the vacuous case (no tail after action point m). The vpos inverse properties are pure sequence identities verified by construction. Foundation usage is consistent — all citations are to ASN-0034 (TumblerAdd, TA0, TA7a, OrdinalShift) and ASN-0036 (S8a), with no reinvented notation.

VERDICT: CONVERGED
