# Review of ASN-0040

## REVISE

### Issue 1: T4 validity is required but not enforced

**ASN-0040, B7 (Namespace Disjointness)**: "provided both parents satisfy T4 and both depths satisfy B6"

**Problem**: B7 states its disjointness guarantee conditionally on T4-valid parents, but nothing in the ASN requires parents to satisfy T4. B6 constrains depth (`d ∈ {1, 2}`) and zeros count but not T4 structural validity. B0a constrains the gate (only baptism adds to B) and references B6, but likewise omits T4. The operational properties (B0a, B2, B4, B6) therefore permit baptisms from non-T4 parents, for which B7 provides no guarantee, and B8 (global uniqueness) becomes unsound.

Concrete counterexample: let p₁ = `[1, 0]` with d₁ = 1 and p₂ = `[1]` with d₂ = 2. Both satisfy B6 — `zeros([1, 0]) + 0 = 1 ≤ 3` and `zeros([1]) + 1 = 1 ≤ 3`. But `[1, 0]` violates T4 (ends in zero). The streams are identical: `inc([1, 0], 1) = [1, 0, 1] = inc([1], 2)`, and all subsequent siblings match, so `S([1, 0], 1) = S([1], 2)`. B7's proviso catches this — T4 fails for `[1, 0]` — but nothing prevents baptism from `[1, 0]` in the first place.

**Required**: Three additions:

(a) Add T4 validity of the parent as an explicit precondition in B6: `d ∈ {1, 2}`, **p satisfies T4**, and `zeros(p) + (d − 1) ≤ 3`.

(b) Require B₀ elements to satisfy T4. Add to B₀ conformance: `(A t ∈ B₀ : t satisfies T4)`.

(c) State the derived guarantee: `(A t ∈ Σ.B : t satisfies T4)` — by induction from (b) and IncrementPreservesValidity (ASN-0034), with (a) ensuring each baptism's output inherits T4 from its parent. This closes the chain: parent ∈ Σ.B → parent satisfies T4 → B7 applies unconditionally to all baptized parents → B8 holds.

### Issue 2: Freshness derivation omits streamless seed elements

**ASN-0040, wp analysis**: "Within namespace (p, d), B1 ensures... In any other namespace (p', d'), B7 ensures... Together, B1 and B7 guarantee freshness."

**Problem**: B is not exhausted by the union of all namespace streams. B₀ may contain elements not in any S(p', d') — root addresses like `[1]` that have no parent (no standard tumbler p exists with `#p + d = 1`). The derivation covers `B ∩ S(p, d)` via B1 and `B ∩ S(p', d')` for other namespaces via B7, but not `B \ ∪ S(p'', d'')`.

The gap is trivially closeable. `c_{hwm+1} ∈ S(p, d)` by construction. Any streamless element `r ∉ S(p'', d'')` for all `(p'', d'')` is in particular not in `S(p, d)`. So `c_{hwm+1} ≠ r`. But this is the third case in a three-case partition of B, and the derivation must show all three.

**Required**: Add the third case to the freshness derivation: "For elements of B not in any namespace stream (root seed elements), `c_{hwm+1} ∈ S(p, d)` by definition and these elements `∉ S(p, d)`, so no collision."

### Issue 3: Citation error in B7 Case 3 verification

**ASN-0040, "A baptism traced"**: "Suppose node [1, 1] has been baptized via inc([1], 1) = [1, 1] (TA5(c))."

**Problem**: TA5(c) is the sibling case (`k = 0`). Here `k = 1 > 0`, so TA5(d) — the child case — applies. TA5(d) with `t = [1]`, `k = 1`: `#t' = 2`, zero intermediate zeros (`k − 1 = 0`), position 2 set to 1. Result `[1, 1]`. The computation is correct; the citation is wrong.

**Required**: Change "(TA5(c))" to "(TA5(d))".

## OUT_OF_SCOPE

None. The ASN's open questions section already identifies the relevant deferred topics — parent prerequisite chain, valid seed sets, distributed coordination, canonical depth, minimal serialization grain, subspace partitioning.

VERDICT: REVISE
