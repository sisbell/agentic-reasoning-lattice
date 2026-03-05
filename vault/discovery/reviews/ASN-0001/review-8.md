# Review of ASN-0001

## REVISE

### Issue 1: TA4 formal statement is missing a necessary precondition
**ASN-0001, Tumbler arithmetic / Inverse**: "(A a, w : w > 0 ∧ k = #a ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a), where k is the action point of w."
**Problem**: The constructive verification later in the same section explicitly demonstrates that the inverse fails when `#w > k`: "For multi-component displacements (`#w > k`), the subtraction result has extra trailing components `wₖ₊₁, ...` from `w` beyond position `k`. ... The inverse holds exactly only when `#w = k`." The formal statement of TA4 does not include `#w = k` as a precondition, so the axiom as written claims more than the verification establishes. Concretely: `a = [5]`, `w = [0, 3]` (so `k = 2`, but wait, `k = 2 > #a = 1`, so TA0 blocks this). Let me construct a valid counterexample: `a = [0, 5]`, `w = [0, 3, 7]`. Action point `k = 2`, `#a = 2 = k`, zero-prefix satisfied (`a₁ = 0`). Then `a ⊕ w = [0, 8, 7]`. Now `[0, 8, 7] ⊖ [0, 3, 7]`: divergence at position 2 (`8 ≠ 3`), result = `[0, 5, 7]`. But `a = [0, 5]`, so `(a ⊕ w) ⊖ w = [0, 5, 7] ≠ [0, 5] = a`. TA4 as stated is false.
**Required**: Add `#w = k` (equivalently `#w = #a`) to TA4's precondition. The formal statement should read: `(A a, w : w > 0 ∧ k = #a ∧ #w = k ∧ (A i : 1 ≤ i < k : aᵢ = 0) : (a ⊕ w) ⊖ w = a)`. Update the Properties Introduced table accordingly.

### Issue 2: Reverse inverse corollary proof relies on unfixed TA4
**ASN-0001, Tumbler arithmetic / Inverse**: "Suppose `y ⊕ w ≠ a`. If `y ⊕ w > a`, then applying `⊖ w` to both sides ... gives `a ⊖ w < (y ⊕ w) ⊖ w = y`"
**Problem**: The proof's contradiction argument uses `(y ⊕ w) ⊖ w = y`, citing TA4. It verifies TA4's preconditions for `y`: `k = #y` and `yᵢ = 0` for `i < k`. But TA4 additionally requires `#w = k` (per Issue 1), and this is not verified. When `#w > k`, the proof breaks: `(y ⊕ w) ⊖ w` has trailing components from `w` and does not equal `y`. The same gap affects the `y ⊕ w < a` branch. The reverse inverse corollary is unproven for multi-component displacements.
**Required**: Either (a) add `#w = k` to the reverse inverse corollary's precondition (matching the corrected TA4), or (b) provide a proof that does not depend on TA4 for the general case. The statement of the corollary should be consistent with whichever approach is taken.

### Issue 3: TA3 proof claims five cases but presents four
**ASN-0001, Verification of TA3**: "Five cases arise from the relationship among `j`, `dₐ`, and `d_b`."
**Problem**: Three main cases are presented: `dₐ = d_b`, `dₐ < d_b`, `dₐ > d_b`. Case 1 has two subcases (`j = d` and `j > d`). That is four realizable paths, not five. The impossibility of `j < d` within Case 1 is dismissed inline ("we need `j ≥ d`") but never labeled as a case. The count "five" is unexplained.
**Required**: Either present the claimed five cases (perhaps by explicitly listing the `j < d` dismissal as a vacuous case) or correct the count to match what is shown.

### Issue 4: Constructive definition of ⊖ does not handle `a = w`
**ASN-0001, Constructive definition of ⊕ and ⊖**: "Let `k` be the first position where `a` and `w` differ"
**Problem**: TA2 states that `a ⊖ w` is well-defined when `a ≥ w`, which includes the case `a = w`. When `a = w`, there is no position where they differ — `k` is undefined. The constructive definition does not specify what happens. The natural answer is that the result is the zero tumbler of length `#a` (all positions are "before the divergence" and get zeroed), but this must be stated, since the algorithm as written requires a divergence point to exist.
**Required**: Add an explicit clause: when `a = w`, `a ⊖ w` is the zero tumbler `[0, ..., 0]` of length `#a`. Alternatively, define `k = #a + 1` when no divergence exists, with all positions falling into the "zeroed before divergence" case.

## OUT_OF_SCOPE

### Topic 1: Empty fields in T4
T4 requires every field component to be strictly positive but does not require every field to be non-empty. A tumbler like `[0, 1]` parses with an empty node field (no components before the first zero separator) and a one-component user field `[1]`. This is likely invalid in practice (every address must identify a server) but is not excluded by T4 as stated. Formalizing minimum field-occupancy constraints belongs in a future ASN on address validity.
**Why defer**: T4 correctly captures the parsing structure and the positive-component constraint. Whether fields may be empty is a question about the valid address set, not about the algebra.

### Topic 2: V-space position validity
The ASN states that V-positions "run contiguously from 1 to the document's current length" but does not formalize what constitutes a valid V-position or what invariants the POOM mapping must satisfy. The worked example uses single-component tumblers for V-positions without establishing this as a requirement.
**Why defer**: V-space structure and the POOM mapping are separate specification topics that build on the algebra but are not part of it.

### Topic 3: Crash recovery of allocation counters
Listed in the ASN's own Open Questions. The interaction between T9 (monotonic allocation) and system failure is a liveness and durability concern, not an algebraic one.
**Why defer**: This requires reasoning about system state persistence, not tumbler properties.
