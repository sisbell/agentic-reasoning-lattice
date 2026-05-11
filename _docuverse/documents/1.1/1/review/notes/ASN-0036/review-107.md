# Review of ASN-0036

I worked through the ASN's twelve major claims (S0–S9 plus the D-* contiguity properties and the ord/vpos decomposition lemmas), tracing every proof against its declared dependencies and stress-testing the boundary cases.

## What I checked

**S5 unrestricted sharing.** Both witness constructions exhibit pairwise-distinct documents `dᵢ = [1, 0, 1, 0, i]` and distinct V-positions `[1, k]` via T3; the frame note correctly delimits scope to S0–S3 and acknowledges that S7b/S7c are not established on the abstract `a`.

**ShiftPreservation conclusion (iv).** The position-arithmetic chain `#a − δ + 1 < #a` from `δ ≥ 2` is rigorously derived: `1 < 2 ≤ δ` via NAT-addcompat's successor and NAT-order's mixed transitivity; NAT-addcompat left-compat lifts to `(#a−δ)+1 ≤ (#a−δ)+δ`; NAT-cancel rules out equality (collapse would give `1 = δ`); NAT-sub's right-inverse rewrites to `#a`.

**S8 within-subspace incompatibility lemma.** Both branches (Case `j < m` via T1(i) prefix-copy argument; Case `j = m` via NAT-discrete's `v_m + 1 ≤ t_m` against `t_m < v_m + 1 = shift(v,1)_m` using NAT-order's exactly-one trichotomy) yield contradictions. Cross-subspace uniqueness via T5 + T10 with `[S₁] ⋠ [S₂] ∧ [S₂] ⋠ [S₁]` from T3 on distinct length-1 prefixes.

**OrdAddHom boundary cases.** At `k = 2` the first range `1 ≤ j < k−1` collapses to `1 ≤ j < 1` (empty prefix copy); at `k = m` the third range `k−1 < j ≤ m−1` collapses (empty tail copy). Both verified component-by-component.

**OrdAddS8a equivalence chain.** Step (a) reduces S8a on `v ⊕ w` to componentwise positivity, step (b) discharges position 1 unconditionally from `w₁ = 0 ⟹ k ≥ 2`, step (c) chains via reindexing `j = i − 1` to `ord(v⊕w) ∈ S`. Action-point component `rₖ ≥ 2` derived correctly via NAT-addcompat at `(1, vₖ, 1)` and `(vₖ, wₖ, 1)`.

**D-CTG-depth.** The constructed intermediate `w` with `wⱼ₊₁ = n` and trailing 1s satisfies S8a explicitly (every component positive) and falls strictly between `v₁` and `v₂` by T1(i); T0(a) (or the alternative NAT-closure injection in the parenthetical) produces infinitely many such w, contradicting S8-fin.

**D-SEQ.** Four steps assembled correctly: shared prefix (m = 2 vacuous, m ≥ 3 via D-CTG-depth), minimum k = 1 (D-MIN), contiguity of k-values (D-CTG with S8a explicitly verified on intermediates), finiteness (S8-fin).

**Worked example k = 3.** `M(d₁)(shift(1.1, 3)) = M(d₁)([1, 4]) = 1.0.1.0.1.0.1.4` and `shift(1.0.1.0.1.0.1.1, 3) = [1,0,1,0,1,0,1,1] ⊕ δ(3, 8) = [1,0,1,0,1,0,1,4]` — both sides equal, exercising ShiftPreservation conclusions (i) and (iv) on a non-trivial k.

## What I found

No hand-waves, no "similarly" proofs, no missing edge cases, no implicit assumptions. Forward references (S7c → ShiftPreservation; subspace_I → ShiftPreservation; subspace → OrdShiftHom) are non-circular — each downstream lemma's dependencies are independent of the referencing definition's postcondition. Dependencies are honestly disclosed, including the acknowledgment that S7b/S7c are vacuous on S8's singleton existence witness and load-bearing only for the run-corollary's `k ≥ 1` content. No cross-ASN references outside the foundation set.

## REVISE

(none)

## OUT_OF_SCOPE

(none — the Open Questions appropriately defer operation-layer concerns, link-subspace semantics, subspace alignment, and TA7a subtraction conditions to future ASNs)

VERDICT: CONVERGED
