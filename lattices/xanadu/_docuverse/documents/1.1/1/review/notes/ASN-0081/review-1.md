# Review of ASN-0081

## REVISE

### Issue 1: D-X contradicts D-SHIFT — postconditions are internally inconsistent

**ASN-0081, D-X and D-SHIFT:**

D-X: `(A v : v ∈ X : v ∉ dom(M'(d)))`

D-SHIFT: `(A v : v ∈ R : σ(v) ∈ dom(M'(d)) ∧ M'(d)(σ(v)) = M(d)(v))`

**Problem:** The shift maps right-region positions onto addresses that fall within X. At depth 2, σ(v) = [S, v₂ − c]. By D-SEP, the minimum shifted ordinal is p₂ = ord(p). Since X contains all positions with ordinals in [p₂, p₂ + c − 1], the shifted positions in Q₃ reuse addresses that belonged to X. D-X says these addresses are absent from dom(M'(d)); D-SHIFT says they are present.

Concrete counterexample: arrange [1,1]→i₁ through [1,5]→i₅. Contract at p = [1,2], w = [0,2], so r = [1,4].

- X = {[1,2], [1,3]},  R = {[1,4], [1,5]}
- σ([1,4]) = vpos(1, [4] ⊖ [2]) = [1,2]
- σ([1,5]) = vpos(1, [5] ⊖ [2]) = [1,3]
- D-X: [1,2] ∉ dom(M'(d)).  D-SHIFT: [1,2] ∈ dom(M'(d)).  Contradiction.

The correct post-state is [1,1]→i₁, [1,2]→i₄, [1,3]→i₅. The addresses [1,2] and [1,3] ARE in dom(M'(d)) — they hold shifted content, not the original X mappings.

**Required:** Replace D-X. The pre-state mapping at X positions is not preserved, but the addresses themselves are reused by shifted content. Two options:

(a) Weaken D-X to: `(A v ∈ X : ¬(v ∈ dom(M'(d)) ∧ M'(d)(v) = M(d)(v)))` — the original mapping at v is not preserved (but v may appear in dom(M'(d)) with a different mapping from the shift).

(b) Drop D-X entirely and replace it with the closed-world postcondition from Issue 4 below, from which removal of X's pre-state mappings follows implicitly.

### Issue 2: Missing contiguity precondition for V_S(d)

**ASN-0081, D-SEP and D-DP:**

D-SEP: "the minimum shifted ordinal equals ord(p)"

D-DP proof: "By D-SEP, σ(r) has ordinal ord(p)"

**Problem:** Both claims apply σ to r and require r ∈ R, i.e., r ∈ V_S(d). Nothing in the stated preconditions guarantees this. The contraction setup says the contraction span "lies entirely within the current arrangement," establishing X ⊆ V_S(d) — but this says nothing about r, the exclusive upper bound of the span.

If V_S(d) has gaps, r might not be allocated. Then min(R) > r, the minimum shifted ordinal exceeds ord(p), and the gap-closure claim fails.

The algebraic identity ord(r) ⊖ w_ord = ord(p) is correct regardless, but the semantic interpretation as gap closure requires r ∈ V_S(d).

**Required:** Add a local axiom or precondition establishing contiguity. Either:

(a) Local axiom: V_S(d) is order-contiguous within subspace S — for any v₁, v₂ ∈ V_S(d) with subspace(v₁) = subspace(v₂) = S and v₁ < v₂, every element-level address v with v₁ ≤ v ≤ v₂ and subspace(v) = S is in V_S(d). This is a natural structural consequence of sequential allocation within a subspace.

(b) Separate the algebraic identity from the gap-closure claim: D-SEP proves ord(r) ⊖ w_ord = ord(p); a separate corollary derives gap closure from the identity plus contiguity (or plus R ≠ ∅ ⟹ r = min(R)).

### Issue 3: D-DP proof cites D-X where D-X is contradicted

**ASN-0081, D-DP proof:**

"No ordinal between max(L) and min(Q₃) goes unaccounted for — positions in that range belonged to X and are intentionally removed (D-X)."

**Problem:** Two issues with this sentence:

(a) At depth 2 with contiguous allocation, max(L) has ordinal p₂ − 1 and min(Q₃) has ordinal p₂. There are no ordinals strictly between p₂ − 1 and p₂. The claim is vacuously true — no citation of D-X is needed.

(b) Positions at ordinals [p₂, p₂ + c − 1] are not "removed" from dom(M'(d)) — they are occupied by shifted R content per D-SHIFT (as shown in Issue 1). Citing D-X compounds the inconsistency.

**Required:** Rewrite the gap-closure argument without D-X. The correct reasoning: L has ordinals below p₂ (by definition), Q₃ begins at ordinal p₂ (by D-SEP + contiguity). The ordinals p₂ − 1 and p₂ are consecutive; no ordinal falls between them.

### Issue 4: Missing closed-world postcondition

**ASN-0081, Region Postconditions section:**

**Problem:** D-L, D-SHIFT, D-CS, and D-CD individually constrain M'(d) but do not jointly pin down its domain. No postcondition states:

`dom(M'(d)) ∩ V_S(d) = L ∪ Q₃`

Without this, additional V-positions could appear in M'(d) within subspace S without violating any stated postcondition. The specification under-determines M'(d).

**Required:** Add a domain postcondition:

`dom(M'(d)) ∩ V_S(d) = L ∪ Q₃`

Combined with D-L and D-SHIFT, this fully characterizes M'(d) within subspace S: positions in L retain their original mappings, positions in Q₃ hold shifted mappings from R, and no other positions exist. This also subsumes a corrected D-X — the removal of X's original mappings follows from X ∩ (L ∪ Q₃) containing only addresses whose mappings have changed.

### Issue 5: No concrete example

**ASN-0081, entire ASN:**

**Problem:** The ASN proves all results abstractly but never verifies them against a specific scenario. A worked example would have immediately exposed the D-X/D-SHIFT contradiction.

**Required:** Include at least one concrete example. Suggested: 5-position arrangement [1,1]→i₁ through [1,5]→i₅, contract at [1,2] with width [0,2]. Show the three-region partition, compute σ for each v ∈ R, display the post-state arrangement, and verify D-L, D-SHIFT, D-BJ, D-SEP, and D-DP against the concrete result.

## OUT_OF_SCOPE

### Topic 1: Generalization to ordinal depth > 1
**Why out of scope:** Explicitly acknowledged in the ASN's Open Questions. The scoping axiom restricts to depth 2 where TA4's zero-prefix condition is vacuously satisfied and TA3-strict's equal-length precondition holds trivially. Deeper ordinals require fresh analysis of these preconditions — future work, not a defect in this ASN.

### Topic 2: Fate of I-addresses at deleted V-positions
**Why out of scope:** When X positions are removed from the arrangement, their I-addresses remain permanent (T8) and may still be referenced by links or transclusions elsewhere. Tracking consequences for link discoverability and transclusion integrity is link-ontology territory, not span algebra.

VERDICT: REVISE
