# Cone Review — ASN-0036/ValidInsertionPosition (cycle 1)

*2026-04-13 17:06*

### TumblerAdd cited as proof substrate without foundation import

**Foundation**: OrdinalShift (ShiftDefinition, ASN-0034) — definition uses `v ⊕ δ(n, m)` but exports postconditions that absorb TumblerAdd's behavior
**ASN**: S8-depth — "the action point of δ(k, #a) is #a"; ValidInsertionPosition — "since δ(j, m) has action point m and m ≥ 2, TumblerAdd copies components 1 through m − 1 unchanged and sets the last component to 1 + j"; empty-case proof — "the action point of [1] is k = 1, so TumblerAdd gives r₁ = S + 1"
**Issue**: The ASN cites TumblerAdd by name and reasons through its internal structure — the δ(n, m) vector, its "action point," and componentwise addition semantics — at seven distinct points across S8-depth and ValidInsertionPosition. TumblerAdd is not in the foundation statements, and "action point" is defined nowhere in the cited foundations. Every claim the ASN derives via TumblerAdd is independently derivable from OrdinalShift's exported postconditions (prefix preservation: `shift(v,n)ᵢ = vᵢ` for `i < m`; last-component increment: `shift(v,n)ₘ = vₘ + n`), but the proofs as written go through TumblerAdd's internal structure rather than OrdinalShift's interface.
**What needs resolving**: Either import TumblerAdd as a foundation with its action-point definition and δ-vector semantics, or restate the seven proof steps to use only OrdinalShift postconditions without referencing TumblerAdd, δ vectors, or action points by name.

---

### D-MIN postcondition notation assumes m ≥ 2 without guard

**Foundation**: D-MIN axiom, D-CTG invariant, S8-fin, S8-depth
**ASN**: D-MIN postcondition — "Combined with D-CTG and S8-fin, `V_S(d) = {[S, 1, …, 1, k] : 1 ≤ k ≤ n}` for some finite n ≥ 1. Positions within a subspace differ only at the last component and form a contiguous range starting at 1."
**Issue**: The derivation handles m = 2 ("trivially") and m ≥ 3 (via the D-CTG depth-≥-3 postcondition) but never addresses m = 1. At depth 1, the notation `[S, 1, …, 1, k]` collapses: the subspace identifier S and the varying ordinal k occupy the same (only) component position. For S = 2, the postcondition predicts `V_S(d) = {[k] : 1 ≤ k ≤ n}`, which includes `[1]` — a position in subspace 1, not subspace 2. The notation requires at least two components to keep the subspace identifier and the ordinal in distinct positions, but the formal postcondition states no m ≥ 2 guard.
**What needs resolving**: The postcondition either needs an explicit m ≥ 2 guard, or the derivation needs a separate m = 1 case establishing that `V_S(d) = {[S]}` (exactly one position where the subspace identifier is the only component and no independent ordinal exists).

---

### V-position depth ≥ 2 is derivable but never stated

**Foundation**: S8a (V-positions are element-field tumblers), S3 (ReferentialIntegrity), S7c (element-field depth δ ≥ 2)
**ASN**: S8-depth — guards postcondition 1 on `#v ≥ 2`, discusses failure at `#v = 1`; ValidInsertionPosition — states `m ≥ 2` as a precondition, gives two paragraphs of m = 1 failure analysis; D-MIN postcondition — notation implicitly requires m ≥ 2
**Issue**: S8a establishes that each V-position v is the element field of M(d)(v). S3 guarantees M(d)(v) ∈ dom(Σ.C). S7c guarantees `#fields(a).element ≥ 2` for such addresses. Combining these three: `#v ≥ 2` for every V-position in every populated subspace. This three-step chain is never assembled. Instead, `m ≥ 2` appears as an apparently independent precondition in ValidInsertionPosition, as a guard in S8-depth postcondition 1, and as an implicit assumption in D-MIN's postcondition derivation. The ASN devotes substantial text to m = 1 failure modes (subspace-identity breakdown in both S8-depth and ValidInsertionPosition), treating depth 1 as a live concern — when it is structurally impossible for any V-position that participates in M(d). (For the empty-subspace case in ValidInsertionPosition, m ≥ 2 remains a genuine design constraint, but it is separately justified by compatibility with S7c's element-field depth requirement.)
**What needs resolving**: State `#v ≥ 2` as a derived property of V-positions (from S8a + S3 + S7c), then simplify the downstream chain: D-MIN's postcondition holds without a depth caveat for populated subspaces, ValidInsertionPosition's non-empty case inherits m ≥ 2 as a theorem rather than a guard, and S8-depth postcondition 1 loses its parenthetical exception.
