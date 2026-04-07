# Review of ASN-0061

## REVISE

### Issue 1: D-DEL is a false postcondition
**ASN-0061, Effect on the Arrangement / D-DEL**: "(A v : v ∈ X : v ∉ dom(M'(d)))"
**Problem**: This claims every V-position in the deleted interval X is absent from dom(M'(d)). The ASN's own worked example refutes it. In the example, X = {[1,2], [1,3]} and Q₃ = {σ([1,4]), σ([1,5])} = {[1,2], [1,3]}. The post-state table shows [1,2] → b+3 and [1,3] → b+4 — both positions are in dom(M'(d)). Whenever R ≠ ∅, the shifted right-region positions σ(v) start at ordinal ord(p) (by D-SEP), which is the first ordinal of X. So Q₃ ∩ X ≠ ∅ whenever |R| ≥ 1, and D-DEL is violated.

The downstream proofs (D-DP, D-BLK, invariant preservation) are unaffected — they work with Q₂ = L and Q₃ directly, never through D-DEL. The specification's intent is clear: the *original mappings* at X positions are discarded, but the V-positions may be reoccupied by shifted content. D-DEL as a formal postcondition states the wrong thing.

**Required**: Replace D-DEL with a statement that correctly distinguishes "original mapping removed" from "V-position absent." For example: "For every v ∈ X, the mapping M(d)(v) does not persist in M'(d). If v ∈ dom(M'(d)), then v ∈ Q₃ and M'(d)(v) is determined by D-SHIFT — a different I-address from M(d)(v)." Alternatively, drop D-DEL as a standalone postcondition; the post-state is already fully determined by D-LEFT, D-SHIFT, D-XS, and domain completeness (dom(M'(d)) ∩ V_S = L ∪ Q₃).

### Issue 2: D-ORPH missing within-subspace sharing condition
**ASN-0061, Content Orphaning / D-ORPH**: "if a ∈ ran(M_S(d)), a maps from a position v ∈ X ... a ∉ ran(M_{S'}(d)) for all S' ≠ S, and a ∉ ran(M(d')) for all d' ≠ d, then after DELETE, a is orphaned."
**Problem**: The conditions check cross-subspace and cross-document references but do not check within-subspace sharing (S5, ASN-0036; M13, ASN-0058). If a maps from both v₁ ∈ X and v₂ ∈ L (same subspace, same document), then v₂ survives and a ∈ ran(M'_S(d)) — not orphaned. The proof step "By D-DEL, v is removed from dom(M'(d)), so a ∉ ran(M'_S(d))" does not follow: removing one V-position that maps to a does not remove a from the range when other V-positions also map to a.
**Required**: Add the condition `(A v' : v' ∈ V_S(d) ∧ M(d)(v') = a : v' ∈ X)` — every V-position in the same subspace mapping to a must be in the deleted interval.

### Issue 3: D-PRE formal items incomplete
**ASN-0061, Precondition / D-PRE**: Items (i)–(v) omit two constraints that are stated in the surrounding prose and used in proofs: `#w = #p` (same depth) and `w₁ = 0` (subspace preservation).
**Problem**: These constraints are load-bearing. Without `w₁ = 0`, TumblerAdd at action point k = 1 would shift the subspace identifier (r₁ = p₁ + w₁ ≠ S). Without `#w = #p`, the action point of w might exceed #p, violating TA0. Both constraints are stated clearly in prose before D-PRE, but the formal precondition labeled "D-PRE — DeletePrecondition (PRE)" should be self-contained.
**Required**: Add items to D-PRE: (vi) `#w = #p`, (vii) `w₁ = 0`.

### Issue 4: Block classification claims five exhaustive cases but six exist
**ASN-0061, Block Decomposition Effect**: "Exactly one of five conditions holds: (a)...(e)"
**Problem**: A block with `v < p` and `v_end > r` (straddling both cut points) satisfies none of (a)–(e). Case (b) requires `v_end ≤ r`; case (d) requires `p ≤ v`. The ASN acknowledges this sixth case in a subsequent paragraph ("A block may straddle both cuts") and handles it correctly in D-BLK, but the "exactly one of five" claim is mathematically false.
**Required**: Either add case (f): "Straddles both cuts: `v < p` and `v_end > r`" and change "five" to "six", or restructure the enumeration to subsume the both-cuts case.

## OUT_OF_SCOPE

### Topic 1: Ordinal extraction as foundation definitions
The functions ord(v), vpos(S, o), and w_ord are introduced here but will be needed by INSERT, COPY, and REARRANGE. They are natural companions to TA7a (ASN-0034) and could be promoted to the tumbler algebra or a shared foundation ASN.
**Why out of scope**: This is a structural improvement for reuse, not an error in ASN-0061.

### Topic 2: Generalization beyond ordinal depth 1
The depth restriction D-PRE(iv) (#p = 2) is explicitly stated and the open questions correctly identify generalization as future work. At depth > 1, TA4's zero-prefix precondition is not vacuously satisfied, and the commutativity σ(v) + j = σ(v + j) requires a separate argument. The ASN is honest about this boundary.
**Why out of scope**: The ASN correctly scopes its claims; deeper ordinals are new territory.

VERDICT: REVISE
