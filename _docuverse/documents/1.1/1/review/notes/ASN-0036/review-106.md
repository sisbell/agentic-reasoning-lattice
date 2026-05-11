# Review of ASN-0036

## REVISE

(No REVISE items — the ASN is in solid shape.)

## OUT_OF_SCOPE

### Topic 1: Link subspace (S = 2) contiguity semantics
**Why out of scope**: The ASN explicitly defers link-subspace structural properties (sparse, append-only with tombstones) to a future ASN. D-CTG, D-MIN, D-CTG-depth, D-SEQ are all bound to S = 1.

### Topic 2: D-CTG/D-MIN preservation by editing operations
**Why out of scope**: Whether DELETE/INSERT/COPY/REARRANGE preserve text-subspace contiguity is the verification obligation of each operation's ASN (Open Question 7), not of the strand model.

### Topic 3: Subspace alignment (subspace(v) = subspace_I(M(d)(v)))
**Why out of scope**: The Remark after S8a explicitly deflects this to the operations layer, citing Nelson's architectural treatment and Gregory's unconditional `acceptablevsa`.

### Topic 4: Canonical depth choice for empty subspaces (m beyond ≥ 2)
**Why out of scope**: Open Question 9 — the operational input m in ValidFirstInsertionPosition is a one-time convention chosen by the placing operation; the strand model fixes only m ≥ 2.

---

**Notes on verification (no action required)**

Verified soundness of:
- ShiftPreservation's four conclusions (i)–(iv), including the position-arithmetic step `#a − δ + 1 < #a` from S7c via NAT-sub/addcompat/order/cancel.
- S8's within-subspace incompatibility lemma, both cases `j < m` and `j = m` (the latter using NAT-discrete and the trichotomy disjointness clause).
- S8's cross-subspace uniqueness via T5 + T10 with non-nesting single-component prefixes.
- OrdAddHom's three-region match, including the boundary regimes `k = 2` and `k = m` collapsing the prefix/tail copy ranges.
- OrdAddS8a's equivalence chain reducing S8a-on-`v⊕w` to positivity of `w`'s tail past the action point.
- D-CTG-depth's contradiction-by-infinitely-many-intermediates, including the T0(a)-iteration form and the alternative explicit-injection form (the strict-lifting via NAT-cancel is correctly identified in the Depends list).
- D-SEQ's three-step assembly (shared prefix, minimum k = 1, contiguity of k-values).
- S8's run-corollary correctly cites ShiftPreservation pointwise for `k ≥ 1` and the identity for `k = 0`.
- Worked example's k = 3 shift verification at depth 8.

VERDICT: CONVERGED
