# Review of ASN-0058

## REVISE

### Issue 1: Ordinal decrement via TumblerSub is broken for multi-component tumblers

**ASN-0058, M12 (CanonicalUniqueness)**: "We write `v − 1` for the ordinal decrement `v ⊖ w₁` where `w₁ = [0, ..., 0, 1]` has length `#v`."

**Problem**: TumblerSub (ASN-0034) finds the *first* position where `v` and `w₁` differ and subtracts there. For any V-position with more than one component (e.g., `v = [1, 5]` with subspace identifier 1 and ordinal 5), the first divergence is at position 1 — because `v₁ > 0` and `(w₁)₁ = 0`. TumblerSub then computes `v₁ - 0 = v₁` at position 1 and copies the rest, returning `v` unchanged.

Concrete witness: `v = [1, 5]`, `w₁ = [0, 1]`. TumblerSub: divergence at `k = 1`, result `[1 - 0, 5] = [1, 5] = v`. The intended predecessor `[1, 4]` is never produced.

This is confirmed by TA4 (PartialInverse), which guarantees `(a ⊕ w) ⊖ w = a` *only* when all components of `a` before the action point are zero. S8a (ASN-0036) requires all V-position components strictly positive, so TA4's precondition is never satisfied for text-subspace V-positions with `#v > 1`.

The same failure applies to I-addresses: for full element-level `a` (zeros(a) = 3), `a ⊖ w₁` diverges at position 1 (where the node field is nonzero) and returns `a`.

**Consequences for the proof**:

- Maximal run condition 2 — "`v − 1 ∉ dom(f) ∨ f(v − 1) ≠ a − 1`" — collapses. With `v − 1 = v` and `a − 1 = a`, condition 2 becomes `v ∉ dom(f) ∨ f(v) ≠ a`, i.e., `a ≠ a`, which is always false. Every run "can be extended left," so no maximal runs exist — contradicting the partition claim.

- The claim "when the last component of `v` equals 1, `v ⊖ w₁` has a zero in the element field" is incorrect for `#v > 1`. For `v = [1, 1]`: `[1, 1] ⊖ [0, 1] = [1, 1]`, no zero produced. The claim holds only for single-component tumblers (`[1] ⊖ [1] = [0]`).

- The ⟹ direction's leftward argument ("some block β'' covers `v − 1`") breaks: with `v − 1 = v`, `β''` covering `v` is just `β` itself, and the proof cannot distinguish the predecessor from the current position.

**Required**: Define the ordinal predecessor without TumblerSub. Two options:

(a) Direct definition: `pred(v) = [v₁, ..., v_{m-1}, v_m - 1]` when `v_m ≥ 2`; undefined when `v_m = 1` (result would have a zero component, outside `dom(M(d))` by S8a). Verify `pred(v) + 1 = v` by TumblerAdd: `[v₁, ..., v_m - 1] ⊕ [0, ..., 0, 1] = [v₁, ..., v_m]` at action point `m`. This does not use TumblerSub.

(b) Subtraction-free reformulation: replace condition 2 with "there is no `(v', a')` with `v' + 1 = v` and `a' + 1 = a` and `f(v') = a'`." This uses only TumblerAdd, which is correct at all depths.

---

### Issue 2: M-aux domain omits k = 0

**ASN-0058, M-aux (OrdinalIncrementAssociativity)**: "For any tumbler `v` and natural numbers `c, j`: `(v + c) + j = v + (c + j)`"

**Problem**: The derivation applies TA-assoc to `(v ⊕ w_c) ⊕ w_j = v ⊕ (w_c ⊕ w_j)`, then shows `w_c ⊕ w_j = w_{c+j}`. Both applications of `⊕` require positive displacements (TA0: `w > 0`). When `c = 0` or `j = 0`, `w_0 = [0, ..., 0]` is a zero tumbler, and TA0 is not satisfied. The derivation covers only `c, j ≥ 1`.

The mapping block definition uses `{(v + k, a + k) : 0 ≤ k < n}`, requiring `v + 0 = v`. M5's verification sets `j = 0` in the right half-block. ASN-0036 S8's correspondence run notes "At `k = 0` this is the base case `M(d)(v) = a` — no displacement, no arithmetic," implicitly treating `v + 0 = v` as convention — but ASN-0058's M-aux claims to derive it via TA-assoc, which does not cover the zero case.

**Required**: State `v + 0 = v` explicitly as a notational convention (identity of ordinal shift). Restrict M-aux's TA-assoc derivation to `c, j ≥ 1`, or handle the boundary cases (`c = 0` or `j = 0`) as trivial applications of the identity convention.

---

### Issue 3: M0 injectivity argument cites TA5(a) without establishing equivalence

**ASN-0058, M0 (WidthCoupling)**: "By TA5(a) (ASN-0034), each ordinal increment is strictly increasing: `v + j < v + k` for all `0 ≤ j < k < n`, so the `n` values in `V(β)` are distinct."

**Problem**: TA5(a) states `t' > t` for the operation `inc(t, k)`. The ASN defines `v + k` as `v ⊕ w_k` (TumblerAdd with a displacement), not as iterated `inc(·, 0)`. The two are equivalent — both produce `[v₁, ..., v_m + k]` — but this equivalence is never established. The injectivity follows more directly: by TumblerAdd, `v + j = [v₁, ..., v_m + j]` and `v + k = [v₁, ..., v_m + k]`; when `j ≠ k`, these differ at component `m`, so `v + j ≠ v + k` by T3 (CanonicalRepresentation). Strict ordering follows from T1 at the last component.

**Required**: Either establish the equivalence between `v ⊕ w_k` and `k`-fold `inc(·, 0)`, or derive injectivity directly from TumblerAdd + T3 without citing TA5(a).

---

### Issue 4: M16 cites T10 but T10 does not apply when origins are prefix-comparable

**ASN-0058, M16 (CrossOriginMergeImpossibility)**: "By T10 (PartitionIndependence, ASN-0034), addresses under disjoint document prefixes occupy disjoint subtrees of the tumbler space, confirming the impossibility."

**Problem**: T10 requires `p₁ ⋠ p₂ ∧ p₂ ⋠ p₁` — the prefixes must be incomparable. Document origins can be prefix-comparable: if document `D₁` has field `[3]` and `D₂` has field `[3, 4]`, then `origin₁ = N.0.U.0.3` is a proper prefix of `origin₂ = N.0.U.0.3.4`. T10 does not apply in this case.

The conclusion of M16 is still correct: `a₁ + n₁` and `a₂` differ because their field structures diverge at the position following the shorter document field (one has a field separator, the other has a document-field component). But this follows from T4 field parsing and T3, not from T10.

More simply: `origin` is a function on tumblers. `origin(a₁ + n₁) = origin(a₁) ≠ origin(a₂)`, so by contrapositive `a₁ + n₁ ≠ a₂`.

**Required**: Replace the T10 citation with the contrapositive argument (different origins implies different addresses), or restrict the claim to incomparable origins and handle the prefix-comparable case separately.

## OUT_OF_SCOPE

### Topic 1: Whether V-position ordinals are always single-component
**Why out of scope**: S8-depth (ASN-0036) permits arbitrary tumbler depth for V-positions. The ASN's worked example uses depth-2 V-positions `[1, k]` (single-component ordinals after the subspace identifier), but multi-component ordinals like `[1, 3, 7]` are not excluded. Several properties (M-aux, M0, M1) work correctly at any depth, but the ordinal decrement issue (REVISE #1) is depth-sensitive. A future ASN establishing V-position allocation conventions could resolve whether multi-component ordinals arise in practice.

VERDICT: REVISE
